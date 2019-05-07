from lfcomlib.Jessica import requests, os, time, sqlite3, subprocess, configparser, pymysql, codecs, parse, DaPr, Msg


class Infra:

    def OpenDir(self, Dir):
        os.system("explorer %s" % DaPr.ReplaceDirSlash(Dir))

    def OpenFile(self, Program, Dir, Param):
        if Param == None:
            ParamX = ' '
        else:
            ParamX = Param
        os.system("{} {} {}".format(Program, DaPr.ReplaceDirSlash(Dir), ParamX))

    def StartExe(self, Path, Program):
        os.system("start {}".format(os.path.join(Path, Program)))

    def PostWR(self, DataSource, Parameter):
        Counter = 0
        Response = self.Post(DataSource, Parameter)
        while Response == False:
            time.sleep(1)
            if Counter == 10:
                if input("已经尝试10次是否继续?(y/n)") in ['y', 'Y']:
                    Counter = 0
                    Response = self.Post(DataSource, Parameter)
                else:
                    break
            else:
                Response = self.Post(DataSource, Parameter)
                Counter += 1
        else:
            return Response

    def GetWR(self, DataSource, Parameter):
        Counter = 0
        Response = self.Get(DataSource, Parameter)
        while Response == False:
            time.sleep(1)
            if Counter == 10:
                if input("已经尝试10次是否继续?(y/n)") in ['y', 'Y']:
                    Counter = 0
                    Response = self.Get(DataSource, Parameter)
                else:
                    break
            else:
                Response = self.Get(DataSource, Parameter)
                Counter += 1
        else:
            return Response

    def Post(self, DataSource, Parameter):
        try:
            # 构造并发送Post请求
            Request = requests.post(DataSource, Parameter)
            # 定义返回数据变量名称
            Response = Request.json()
            # 返回响应报文
            return Response
        except:
            # 输出"无网络连接"消息
            print(Msg.NoNetWorkConnection)
            time.sleep(5)
            # 返回 Main.Flow(sel返回到方法
            return False

    def Get(self, DataSource, ParameterDict):
        try:
            # 构造并发送Get请求(在APIUrl后加入查询参数的字典)
            Request = "%s?%s" % (DataSource, parse.urlencode(ParameterDict))
            # Request = RawRequest.encode("utf-8")
            # print(Request)
            # 定义返回报文变量名称
            Response = requests.get(Request)
            return Response
        except:
            # 输出"无网络连接"消息
            print(Msg.NoNetWorkConnection)
            # time.sleep(5)
            # 返回 Main.Flow(sel返回到方法
            return False

    def MariaDBExpress(self, SQL, Data, NumberOfRow, ):
        try:
            from serverConfig.init import globalsetting
            return self.MariaDB(SQL, globalsetting.mariaHost, globalsetting.mariaPort,
                                 globalsetting.mariaUser, globalsetting.mariaPassword,
                                 globalsetting.mariaDatabase, globalsetting.mariaCharSet, Data, NumberOfRow, )
        except Exception as e:
            print(e)
            return False

    def MariaDB(self, SQL, Host, Port, User, Password, Database, CharSet, Data, NumberOfRow, ):
        try:
            # 连接MySQL数据库
            ConnectDataBase = pymysql.connect(host=Host, port=Port, user=User, password=Password, db=Database,
                                              charset=CharSet, cursorclass=pymysql.cursors.DictCursor)
            # 通过cursor创建游标
            DataBaseCursor = ConnectDataBase.cursor()
            # 执行数据查询
            DataBaseCursor.execute(SQL)
            if Data == "None":
                DataBaseCursor.execute(SQL)
                if NumberOfRow == 1:
                    RawData = DataBaseCursor.fetchone()
                    ConnectDataBase.close()
                    return RawData
                if NumberOfRow > 0:
                    RawData = DataBaseCursor.fetchmany(NumberOfRow)
                    ConnectDataBase.close()
                    return RawData
                else:
                    RawData = DataBaseCursor.fetchall()
                    ConnectDataBase.close()
                    return RawData
            else:
                DataBaseCursor.execute(SQL)
                ConnectDataBase.commit()
                ConnectDataBase.close()
                return True
        except Exception as e:
            print(e)
            return False

    def SQLite3(SQL, Data, OutputType, NumberOfRow, Database):

        try:
            if OutputType != 'Dict':
                ConnectDataBase = sqlite3.connect(Database)
                CursorDataBase = ConnectDataBase.cursor()
                ConnectDataBase.row_factory = Infra.dict_factory
            else:
                ConnectDataBase = sqlite3.connect(Database)
                CursorDataBase = ConnectDataBase.cursor()

            if Data == None:
                SQLS = CursorDataBase.execute(SQL)
                if NumberOfRow == 1:
                    RawData = SQLS.fetchone()
                elif NumberOfRow > 0:
                    RawData = SQLS.fetchmany(NumberOfRow)
                else:
                    RawData = SQLS.fetchall()
                if OutputType == "List":
                    return DaPr.MergeMultiTupleList(object, RawData)
                else:
                    return RawData
            else:
                CursorDataBase.execute(SQL, Data)
                ConnectDataBase.commit()
        except:
            # print("[!!]数据库写入失败请联系yzxia@hitachi-systems.cn")
            return False

    def SQLite3Debug(SQL, Data, OutPutType, NumberOfRow, Database):
        ConnectDataBase = sqlite3.connect(Database)
        CursorDataBase = ConnectDataBase.cursor()

        if Data == None:
            SQLS = CursorDataBase.execute(SQL)
            if NumberOfRow == 1:
                RawData = SQLS.fetchone()
            elif NumberOfRow > 0:
                RawData = SQLS.fetchmany(NumberOfRow)
            else:
                RawData = SQLS.fetchall()
            if OutPutType == "List":
                return DaPr.MergeMultiTupleList(RawData)
            else:
                return RawData
        else:
            CursorDataBase.execute(SQL, Data)
            ConnectDataBase.commit()

    def ExcuteBat(self, BatFilePath, BatFile):
        BatFilePath = os.path.join(BatFilePath, BatFile)
        ExcuetBat = subprocess.Popen("cmd.exe /c" + "%s abc" % BatFilePath, stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT)
        Curline = ExcuetBat.stdout.readline()
        while (Curline != b''):
            # print(Curline.decode('GBK'))
            Curline = ExcuetBat.stdout.readline()
        ExcuetBat.wait()
        # print(ExcuteBat.returncode)
        ExcuetBat.terminate()

    def Readini(ConfigFile, Section, Key):
        ReadConfig = configparser.ConfigParser()
        ReadConfig.read_file(codecs.open(ConfigFile, "r", "utf-8-sig"))
        # ReadConfig.sections()
        ReadConfig.options(Section)
        # ReadConfig.items(Section)
        Value = ReadConfig.get(Section, Key)
        return Value

    def read_ini_as_dict(self,ConfigFile):
        ReadConfig = configparser.ConfigParser()
        ReadConfig.read_file(codecs.open(ConfigFile, "r", "utf-8-sig"))
        Dict = dict(ReadConfig._sections)
        for Key in Dict:
            Dict[Key] = dict(Dict[Key])
        return Dict

    def ado_db_con(self, Mode, Host, DB, User, Passsowrd, Proxy, ProxyPort, SQL, Outputtype):
        ConnParm = {'host': r"%s" % Host,
                    'database': DB,
                    'user': User,
                    'password': Passsowrd}
        ConnParm['connection_string'] = """Provider=SQLOLEDB.1;
        User ID=%(user)s; Password=%(password)s;
        Initial Catalog=%(database)s; Data Source= %(host)s"""
        if len(Proxy) > 1:
            import adodbapi.remote as AdoLib
            ConnParm['proxy_host'] = Proxy
            if len(ProxyPort) > 1:
                ConnParm['proxy_port'] = ProxyPort
            else:
                pass
        else:
            import adodbapi as AdoLib
        Ado = AdoLib.connect(ConnParm)
        AdoCur = Ado.cursor()
        if Mode == 'w':
            try:
                AdoCur.execute(SQL)
                Ado.commit()
                Ado.close()
                return True
            except Exception as err:
                print(err)
                return False
        else:
            if Outputtype == 'Dict':
                AdoCur.execute(SQL)
                Columns = [column[0] for column in AdoCur.description]
                RawData = []
                for Row in AdoCur.fetchall():
                    RawData.append(dict(zip(Columns, Row)))
                Ado.close()
                return RawData
            else:
                AdoCur.execute(SQL)
                RawData = []
                for Row in AdoCur.fetchall():
                    for Rowdata in Row:
                        RawData.append(Rowdata)
                Ado.close()
                return RawData

    def read_json(self, filepath, filename):
        import json
        file = os.path.join(filepath, filename)
        # Reading data from file
        with open(file, 'r') as f:
            configstr = f.read().replace('\\', '\\\\').encode(encoding='utf-8')
            configstr = configstr
            configtmp = json.loads(configstr)
            # config = {k: v.replace('\\\\', '\\') for k, v in configtmp.items()}

            return configtmp

    def write_json(self, filepath, filename, data):
        import json
        file = os.path.join(filepath, filename)
        # Writing JSON data
        with open(file, 'w') as f:
            json.dump(data, f)