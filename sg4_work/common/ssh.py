# -*- coding: utf-8 -*-

import re,time,socket
from robot.utils import seq2str,timestr_to_secs,secs_to_timestr

class SSHCCLIENT(object):
    def __init__(self,host_ip,port,prompt,timeout="10sec",newline='CRLF'):
        try:
            import paramiko     # paramiko模块是基于python实现的SSH远程安全连接,用于SSH远程执行命令,文件传输等功能; paramiko包含两个核心组件:SSHClient和SFTPClient
        except BaseException:
            raise RuntimeError("Can't import paramiko library,can't use ssh function.")

        self.host_ip = host_ip
        self.port = port == '' and 22 or int(port)        # 如果port参数为空就是22,有参数就强制转换为int类型
        self._timeout = float(timestr_to_secs(timeout))   # 将字符串描述转换为float浮点数
        self._newline = None
        self.set_newline(newline.upper().replace('LF','\n').replace('CR','\r'))
        self._prompt = None         # 命令行提示符 "ute@2-16-CLOUD1007:~$ "
        self.set_prompt(prompt)
        self._loglevel = "INFO"

        self.username = None
        self.password = None

        self._pausetime = 0.05
        self.conn_type = "SSH"
        self.device_type = None

        self._channel = None
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    @property  # @property 装饰器用在class的function上,就是把方法变成一个属性供外界调用;还能通过方法内部的定义给这个"属性"加上一些限制
    def connected(self):
        try:
            if not self.channel.active or self.channel.closed:
                return False
            else:
                return True
            # return False if self.channel.closed else True
        except socket.error:
            return False
        except Exception as _:
            return False
        else:
            return True

    @property
    def channel(self):
        """null"""
        if not self._channel:
            self._channel = self.client.invoke_shell()
            # combine stderr to stdout
            self._channel.set_combine_stderr(True)

        return self._channel

    def __str__(self):
        return str(self.host) + ":" + str(self.port) + " DeviceType:" + str(self.device_type) + \
            " Timeout:" + secs_to_timestr(self._timeout) + " " + repr(self)

    def __del__(self):
        """Override ssh.__del__ because it sometimes causes problems"""
        pass

    def set_pausetime(self, pause):
        """Sets the timeout used in read socket response, e.g. "120 sec".

        The read operations will for this time before starting to read from
        the output. To run operations that take a long time to generate their
        complete output, this timeout must be set accordingly.
        """
        old = secs_to_timestr(self._pausetime)
        self._pausetime = float(timestr_to_secs(pause))
        return old

    def set_timeout(self, timeout):
        """Sets the timeout used in read operations to given value represented as timestr, e.g. "120 sec".

        The read operations will for this time before starting to read from
        the output. To run operations that take a long time to generate their
        complete output, this timeout must be set accordingly.
        """
        old = secs_to_timestr(self._timeout)
        self._timeout = float(timestr_to_secs(timeout))
        # self.channel.settimeout(self._timeout)
        return old

    def set_loglevel(self, loglevel):
        """null"""
        old = self._loglevel
        self._loglevel = loglevel
        return old

    def set_newline(self, newline):
        """null"""
        old = self._newline
        self._newline = newline
        return old

    def close_connection(self, loglevel=None):
        """Closes current Ssh connection.

        Logs and returns possible output.
        """
        loglevel = loglevel is None and self._loglevel or loglevel
        self.client.close()
        self.client = None
        self._channel = None
        self._log("Disconnect from %s" % str(self), self._loglevel)

        return

    def login(self, username, password, login_prompt='login: ',
              password_prompt='Password: ', key_filename=None):
        """Logs in to SSH server with given user information.

        The login keyword reads from the connection until login_prompt is
        encountered and then types the username. Then it reads until
        password_prompt is encountered and types the password. The rest of the
        output (if any) is also read and all text that has been read is
        returned as a single string.

        Prompt used in this connection can also be given as optional arguments.
        """
        self.username = username
        self.password = password
        self.key_filename = key_filename

        if key_filename is not None:
            self.client.connect(
                self.host,
                self.port,
                username,
                key_filename=self.key_filename,
                timeout=self._timeout)
        else:
            self.client.connect(
                self.host,
                self.port,
                username,
                password,
                timeout=self._timeout)  # ,
        # allow_agent=False, look_for_keys=False)
        # made ssh to use lastline to search.
        time.sleep(self._pausetime)
        start_time = time.time()
        login_ret = ''
        matched = False
        time.sleep(self._pausetime)
        while time.time() - start_time < int(self._timeout):
            if self.channel.recv_ready():
                c = self.channel.recv(128)
                if c == "":
                    break
                login_ret += c

                login_ret = SshCommon._colorpattern.sub("", login_ret)
                matching_pattern = [pattern for pattern in self._prompt
                                    if pattern.search(login_ret[-80:])]
                if len(matching_pattern) > 0:
                    pattern = matching_pattern[0].pattern
                    matched = True
                    break

                continue
            else:
                time.sleep(0.00005)  # wait for CPU.
                # break
        self._log(login_ret, self._loglevel)
        if not matched:
            raise AssertionError('No match found for prompt "%s" in %ssec, detail info: "%s"'
                                 % (seq2str([x.pattern for x in self._prompt], lastsep=' or '),
                                    timestr_to_secs(self._timeout), login_ret))
        self._log("Select pattern '%s' as default pattern" % pattern)
        self.set_prompt(pattern)
        return login_ret

    def write(self, text):
        """Writes given text over the connection and appends newline"""
        self.write_bare(text)
        self.write_bare(
            r"%s" %
            ("" if self._newline is None else self._newline))

    def write_bare(self, text):
        """Writes given text over the connection without appending newline"""
        try:
            text = str(text)
        except UnicodeError:
            msg = 'Only ascii characters are allowed in ssh. Got: %s' % text
            raise ValueError(msg)

        if text not in (self._newline, ""):
            sDict = {
                chr(3): "Ctrl-C",
                chr(13): "Ctrl-M",
                chr(24): "Ctrl-X",
                chr(25): "Ctrl-Y"}
            self._log(
                "Execute command: " +
                sDict.get(
                    text,
                    text),
                self._loglevel)
        self.channel.sendall(text)

    def read_until(self, expected, timeout):
        """null"""
        data = ''
        time.sleep(self._pausetime)
        start_time = time.time()
        while time.time() < float(timeout) + start_time:
            if self.channel.recv_ready():
                data += self.channel.recv(1)
            else:
                time.sleep(0.00005)
            if data.count(expected) > 0:
                return data
        return data

    def read(self, loglevel=None):
        """Reads and returns/logs everything currently available on the output.

        Read message is always returned and logged but log level can be altered
        using optional argument. Available levels are TRACE, DEBUG, INFO and
        WARN.
        """
        loglevel = loglevel is None and self._loglevel or loglevel
        ret = self.read_very_eager()
        self._log(ret, loglevel)
        return ret

    def read_very_eager(self):
        """null"""
        time.sleep(self._pausetime)
        if self.channel is None:
            return ""
        data = ''
        while self.channel.recv_ready():
            data += self.channel.recv(100000)
        return data

    def read_until_prompt(self, loglevel=None, timeout_add=True):
        """Reads from the current output until prompt is found.

        Expected is a list of regular expressions, and keyword returns the text
        up until and including the first match to any of the regular
        expressions.
        """
        time.sleep(self._pausetime)
        loglevel = loglevel is None and self._loglevel or loglevel
        ret = self.expect(self._prompt, self._timeout)
        if ret[0] == -1:
            self.write('\n')
            ret = self.expect(self._prompt, self._timeout)
            if ret[0] == -1:
                self._log(ret[2], 'WARN')
                raise AssertionError('No match found for prompt "%s" in %ssec, detail info: "%s"'
                                     % (seq2str([x.pattern for x in self._prompt], lastsep=' or '),
                                        timestr_to_secs(self._timeout), ret[2]))
        self._log("Get Response: " + ret[2], loglevel)
        return ret[2]

    def set_prompt(self, *prompt):
        """Sets the prompt used in this connection to 'prompt'.
        'prompt' can also be a list of regular expressions
        """
        old_prompt = self._prompt
        if len(prompt) == 1:
            if isinstance(prompt[0], six.string_types):
                self._prompt = list(prompt)
            else:
                self._prompt = prompt[0]
        else:
            self._prompt = list(prompt)
        indices = list(range(len(self._prompt)))
        for i in indices:
            if isinstance(self._prompt[i], six.string_types):
                self._prompt[i] = re.compile(self._prompt[i], re.MULTILINE)
        return old_prompt

    def get_prompt(self):
        """null"""
        _temp_prompt = []
        if isinstance(self._prompt, six.string_types):
            return self._prompt
        elif type(self._prompt) in (tuple, list):
            _temp_prompt = list(self._prompt)
        else:
            raise TypeError(self.__str__() +
                            " _prompt should be String or List !")
        _temp_prompt_str = []
        for prompt in _temp_prompt:
            if isinstance(prompt, six.string_types):
                _temp_prompt_str.append(prompt)
            else:
                _temp_prompt_str.append(getattr(prompt, "pattern"))
        return _temp_prompt_str

    def _log(self, msg, loglevel=None):
        from robot.libraries.BuiltIn import BuiltIn
        BuiltIn().log(msg)

    _colorpattern = re.compile('|'.join([
        r'\x1b\[\d{1,3}[lhinc]',
        r'\x1b\[\d{1,3};\d{1,3}[lhy]',
        r'\x1b\[\d+[ABCDmgKJPLMincq]',
        r'\x1b\[\d+;\d+[HfmrR]',
        r'\x1b\[[HfmKJic]',
        r'\x1b[DME78=>NOHgZc<ABCDIFGKJ\^_WXV\]]',
        r'\x1b[()][AB012]',
        r'\x1b#\d',
        r'\x1bY\d+',
        r'\x1b\/Z',
        r"\033\[[0-9;]*m"
    ]))

    def expect(self, regexps, timeout=None):
        """null"""
        start_time = time.time()
        data = ''
        regexps = [re.compile(expr) for expr in regexps]
        while time.time() < start_time + int(timeout):
            if self.channel.recv_ready():
                data += self.channel.recv(2000)
            matching_pattern = [pattern for pattern in regexps
                                if pattern.search(data)]
            if len(matching_pattern) > 0:
                pattern = matching_pattern[0]
                data = SshCommon._colorpattern.sub("", data)
                return (regexps.index(pattern), pattern.search(data), data)
            time.sleep(0.5)
        return (-1, None, data)
