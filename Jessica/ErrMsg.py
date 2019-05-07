class ErrMsg:
    UnsupportStr = "不支持输入字符"
    UnableAccessThisFile = "另一个程序正在使用此文件，进程无法访问。"

    def __init__(self, UnsupportStr, UnableAccessThisFile):
        self.UnsupportStr = UnsupportStr
        self.UnableAccessThisFile = UnableAccessThisFile