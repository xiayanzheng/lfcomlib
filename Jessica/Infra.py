from lfcomlib.Jessica import requests, os, time, sqlite3, subprocess, configparser, pymysql, codecs, parse, DaPr, Msg
from lfcomlib.Jessica import psycopg2


class Infra:

    def open_dir(self, selected_dir):
        os.system("explorer %s" % DaPr.ReplaceDirSlash(selected_dir))

    def open_file(self, program, selected_dir, param):
        if param is None:
            param_x = ' '
        else:
            param_x = param
        os.system("{} {} {}".format(program, DaPr.ReplaceDirSlash(selected_dir), param_x))

    def start_exe(self, path, program):
        os.system("start {}".format(os.path.join(path, program)))

    def post_wr(self, data_source, parameter):
        counter = 0
        response = self.post(data_source, parameter)
        while response is False:
            time.sleep(1)
            if counter == 10:
                if input("已经尝试10次是否继续?(y/n)") in ['y', 'Y']:
                    counter = 0
                    response = self.post(data_source, parameter)
                else:
                    break
            else:
                response = self.post(data_source, parameter)
                counter += 1
        else:
            return response

    def get_wr(self, data_source, parameter):
        counter = 0
        response = self.get(data_source, parameter)
        while response is False:
            time.sleep(1)
            if counter == 10:
                if input("已经尝试10次是否继续?(y/n)") in ['y', 'Y']:
                    counter = 0
                    response = self.get(data_source, parameter)
                else:
                    break
            else:
                response = self.get(data_source, parameter)
                counter += 1
        else:
            return response

    def post(self, data_source, parameter):
        try:
            # 构造并发送Post请求
            request = requests.post(data_source, parameter)
            # 定义返回数据变量名称
            response = request.json()
            # 返回响应报文
            return response
        finally:
            # 输出"无网络连接"消息
            print(Msg.NoNetWorkConnection)
            time.sleep(5)
            # 返回 Main.Flow(sel返回到方法
            return False

    def get(self, data_source, parameter_dict):
        try:
            # 构造并发送Get请求(在APIUrl后加入查询参数的字典)
            request = "%s?%s" % (data_source, parse.urlencode(parameter_dict))
            # request = RawRequest.encode("utf-8")
            # print(request)
            # 定义返回报文变量名称
            response = requests.get(request)
            return response
        finally:
            # 输出"无网络连接"消息
            print(Msg.NoNetWorkConnection)
            # time.sleep(5)
            # 返回 Main.Flow(sel返回到方法
            return False

    def db_entry(self, **kwargs):
        from serverConfig.init import globalSetting
        db_name = globalSetting.db_name
        db_config = globalSetting.db_config
        if db_name == "maria":
            try:
                db_config["SQL"] = kwargs['sql']
                db_config["opr_type"] = kwargs['opr_type']
                db_config["NumberOfRow"] = kwargs['number_of_row']
                return self.maria_db(**db_config)
            except Exception as e:
                print(e)
                return False
        elif db_name == "postgres":
            try:
                db_config["sql"] = kwargs['sql']
                db_config["opr_type"] = kwargs['opr_type']
                db_config["NumberOfRow"] = kwargs['number_of_row']
                return self.postgres_db(**db_config)
            except Exception as e:
                print(e)
                return False

    def sqlalcheny_uri_maker(self, **kwargs):
        db_name = kwargs['db_name']
        db_config = kwargs['db_config']
        if db_name in ["maria", "mysql"]:
            '''
            mysql+pymysql://root:hch123@127.0.0.1/lfnova?charset=utf8mb4
            '''
            uri = "{}://{}:{}@{}/{}?charset={}".format(db_config['sql_alchemy'],
                       db_config['User'],
                       db_config['Password'],
                       db_config['Host'],
                       db_config['Database'],
                       db_config['CharSet'])
            print(uri)
            return uri
        elif db_name == "postgres":
            '''
            postgresql+psycopg2://user:password@host/dbname
            '''
            uri = "{}://{}:{}@{}/{}".format(db_config['sql_alchemy'],
                       db_config['User'],
                       db_config['Password'],
                       db_config['Host'],
                       db_config['Database']
                       )
            return uri

    def postgres_db(self, **kwargs):
        print("121321321232")
        opr_type = kwargs['opr_type']
        conn = psycopg2.connect(database=kwargs["Database"],
                                user=kwargs["User"],
                                password=kwargs["Password"],
                                host=kwargs["Host"],
                                port=kwargs["Port"])
        cursor = conn.cursor()
        if opr_type == "update" or opr_type == "insert":
            cursor.execute(kwargs['sql'])
            conn.commit()
            conn.close()
            return True
        elif opr_type == "select":
            print(kwargs['sql'])
            cursor.execute(kwargs['sql'])
            if kwargs['number_of_row'] == 0:
                rows = cursor.fetchall()
                conn.close()
                print(rows)
                return rows
        else:
            return False

    def maria_db(self, **kwargs):
        try:
            # 连接MySQL数据库
            db = pymysql.connect(host=kwargs["Host"],
                                 port=kwargs["Port"],
                                 user=kwargs["User"],
                                 password=kwargs["Password"],
                                 db=kwargs["Database"],
                                 charset=kwargs["CharSet"],
                                 cursorclass=pymysql.cursors.DictCursor)
            # 通过cursor创建游标
            db_cursor = db.cursor()
            # 执行数据查询
            db_cursor.execute(kwargs["SQL"])
            if kwargs["opr_type"] == "select":
                db_cursor.execute(kwargs["SQL"])
                if kwargs["NumberOfRow"] == 1:
                    raw_data = db_cursor.fetchone()
                    db.close()
                    return raw_data
                if kwargs["NumberOfRow"] > 0:
                    raw_data = db_cursor.fetchmany(kwargs["NumberOfRow"])
                    db.close()
                    return raw_data
                else:
                    raw_data = db_cursor.fetchall()
                    db.close()
                    return raw_data
            else:
                db_cursor.execute(kwargs["SQL"])
                db.commit()
                db.close()
                return True
        except Exception as e:
            print(e)
            return False

    def sqlite3(self, sql, data, output_type, number_of_row, database):

        try:
            db = sqlite3.connect(database)
            if output_type != 'Dict':
                db_cursor = db.cursor()
                db.row_factory = self.dict_factory
            else:
                db_cursor = db.cursor()

            if data is None:
                db_instance = db_cursor.execute(sql)
                if number_of_row == 1:
                    raw_data = db_instance.fetchone()
                elif number_of_row > 0:
                    raw_data = db_instance.fetchmany(number_of_row)
                else:
                    raw_data = db_instance.fetchall()
                if output_type == "List":
                    return DaPr.MergeMultiTupleList(object, raw_data)
                else:
                    return raw_data
            else:
                db_cursor.execute(sql, data)
                db.commit()
        finally:
            # print("[!!]数据库写入失败请联系yzxia@hitachi-systems.cn")
            return False

    def sqlite3_debug(self, sql, data, output_type, number_of_row, database):
        db = sqlite3.connect(database)
        if output_type != 'Dict':
            db_cursor = db.cursor()
            db.row_factory = self.dict_factory
        else:
            db_cursor = db.cursor()

        if data is None:
            db_instance = db_cursor.execute(sql)
            if number_of_row == 1:
                raw_data = db_instance.fetchone()
            elif number_of_row > 0:
                raw_data = db_instance.fetchmany(number_of_row)
            else:
                raw_data = db_instance.fetchall()
            if output_type == "List":
                return DaPr.MergeMultiTupleList(raw_data)
            else:
                return raw_data
        else:
            db_cursor.execute(sql, data)
            db.commit()

    def excute_bat(self, bat_file_path, bat_file):
        bat_file_path = os.path.join(bat_file_path, bat_file)
        exe_bat = subprocess.Popen("cmd.exe /c" + "%s abc" % bat_file_path, stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)
        cur_line = exe_bat.stdout.readline()
        while (cur_line != b''):
            # print(cur_line.decode('GBK'))
            cur_line = exe_bat.stdout.readline()
        exe_bat.wait()
        # print(excute_bat.returncode)
        exe_bat.terminate()

    def wcmd(self, command):
        excuet_bat = subprocess.Popen("cmd.exe /c" + "%s abc" % command, stdout=subprocess.PIPE,
                                      stderr=subprocess.STDOUT)
        cur_line = excuet_bat.stdout.readline()
        while (cur_line != b''):
            # print(cur_line.decode('GBK'))
            cur_line = excuet_bat.stdout.readline()
        excuet_bat.wait()
        # print(excute_bat.returncode)
        excuet_bat.terminate()

    def read_ini(self, config_file, section, key):
        read_config = configparser.ConfigParser()
        read_config.read_file(codecs.open(config_file, "r", "utf-8-sig"))
        # ReadConfig.sections()
        read_config.options(section)
        # ReadConfig.items(section)
        value = read_config.get(section, key)
        return value

    def read_ini_as_dict(self, config_file):
        read_config = configparser.ConfigParser()
        read_config.read_file(codecs.open(config_file, "r", "utf-8-sig"))
        dict_data = dict(read_config._sections)
        for Key in dict_data:
            dict_data[Key] = dict(dict_data[Key])
        return dict_data

    def ado_db_con(self, mode, host, db, user, password, proxy, proxy_port, sql, output_type):
        conn_parm = {'host': r"%s" % host,
                     'database': db,
                     'user': user,
                     'password': password}
        conn_parm['connection_string'] = """Provider=SQLOLEDB.1;
        user ID=%(user)s; Password=%(password)s;
        Initial Catalog=%(database)s; Data Source= %(host)s"""
        if len(proxy) > 1:
            import adodbapi.remote as ado_lib
            conn_parm['proxy_host'] = proxy
            if len(proxy_port) > 1:
                conn_parm['proxy_port'] = proxy_port
            else:
                pass
        else:
            import adodbapi as ado_lib
        ado = ado_lib.connect(conn_parm)
        ado_cur = ado.cursor()
        if mode == 'w':
            try:
                ado_cur.execute(sql)
                ado.commit()
                ado.close()
                return True
            except Exception as err:
                print(err)
                return False
        else:
            if output_type == 'Dict':
                ado_cur.execute(sql)
                columns = [column[0] for column in ado_cur.description]
                raw_data = []
                for Row in ado_cur.fetchall():
                    raw_data.append(dict(zip(columns, Row)))
                ado.close()
                return raw_data
            else:
                ado_cur.execute(sql)
                raw_data = []
                for Row in ado_cur.fetchall():
                    for row_data in Row:
                        raw_data.append(row_data)
                ado.close()
                return raw_data

    def read_json(self, filepath, filename):
        import json
        file = os.path.join(filepath, filename)
        # Reading data from file
        with open(file, 'r') as f:
            config_str = f.read().replace('\\', '\\\\').encode(encoding='utf-8')
            config_str = config_str
            config_tmp = json.loads(config_str)
            # config = {k: v.replace('\\\\', '\\') for k, v in config_tmp.items()}

            return config_tmp

    def write_json(self, filepath, filename, data):
        import json
        file = os.path.join(filepath, filename)
        # Writing JSON data
        with open(file, 'w') as f:
            json.dump(data, f)
