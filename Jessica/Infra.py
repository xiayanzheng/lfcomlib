from lfcomlib.Jessica import requests, os, time, sqlite3, subprocess, configparser, pymysql, codecs, parse, DaPr, Msg,sys
from lfcomlib.Jessica import psycopg2, shutil
from lfcomlib.Jessica.Err import logger_i


class Infra:

    def __init__(self):
        self.db_opr_type = {
            "close": "close",
            "insert": "insert",
            "close_commit": "close_commit",
            "update": "update",
            "select": "select"
        }
        self.db_cfg_save = None
        self.db_instance = None
        self.log_cfg = {}

    def rename_ff(self, from_, to_, show_msg=True):
        obj = from_
        if os.path.isdir(obj):
            try:
                os.rename(obj, to_)
            finally:
                pass
            print("Folder {} renamed to {}".format(obj, to_))
        if os.path.isfile(obj):
            os.rename(obj, to_)
            print("File {} renamed to {}".format(obj, to_))

    def remove_ff(self, ff, show_msg=True):
        if os.path.exists(ff):
            if os.path.isdir(ff):
                shutil.rmtree(ff)
                print("Folder {} deleted".format(ff))
            else:
                os.remove(ff)
                print("File {} deleted".format(ff))
        else:
            print("Delete Operation Filed".format(ff))
            return False

    def dir_check(self, dir):
        if not os.path.exists(dir):
            os.makedirs(dir)
            return dir
        else:
            return dir

    def get_folder_size(self, folder):
        folder_size = 0
        for Root, Dirs, Files in os.walk(folder):
            for File in Files:
                folder_size += os.path.getsize(os.path.join(Root, File))
        return folder_size

    def copy_ff(self, from_, to_, show_msg=True):
        if os.path.isdir(from_):
            if not os.path.exists(to_):
                shutil.copytree(from_, to_)
            else:
                print('Folder exists')
                pass
        else:
            to_dir = os.path.split(to_)[0]
            if not os.path.exists(to_dir):
                os.makedirs(to_dir)
            shutil.copy(from_, to_)
        if show_msg:
            print("++++++++++++++++")
            print("From:", from_)
            print("To:", to_)
            print("File {} Copied".format(from_))
            print("++++++++++++++++")

    def copy_ff_with_del(self, from_, to_, show_msg=True):
        if os.path.exists(to_):
            if os.path.isdir(to_):
                shutil.rmtree(to_)
            else:
                os.remove(to_)
        self.copy_ff(from_, to_, show_msg)

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

    def db_entry(self, db=None, db_type=None, **kwargs):
        if db_type in ["maria", "mysql"]:
            if db is None:
                self.db_cfg_save = kwargs
            result = self.maria_db(db, **kwargs)
            counter = 0
            while result in ['conn_lost'] and counter < 10:
                self.db_instance = self.maria_db(db=None, **self.db_cfg_save)
                result = self.maria_db(self.db_instance, **kwargs)
                counter += 1
                if counter == 10:
                    print("DB connection lost")
                    break
            return result
        elif db_type == "postgres":
            return self.postgres_db(db, **kwargs)

    def sqlalcheny_uri_maker(self, **kwargs):
        db_type = kwargs['db_type']
        db_config = kwargs['db_config']
        if db_type in ["maria", "mysql"]:
            '''
            mysql+pymysql://root:hch123@127.0.0.1/lfnova:3306?charset=utf8mb4
            '''
            uri = "{}://{}:{}@{}:{}/{}?charset={}".format(db_config['db_sql_alchemy'],
                                                          db_config['db_user'],
                                                          db_config['db_pass'],
                                                          db_config['db_host'],
                                                          db_config['db_port'],
                                                          db_config['db_name'],
                                                          db_config['db_char'])
            return uri
        elif db_type == "postgres":
            '''
            postgresql+psycopg2://user:password@host:5230/dbname
            '''
            uri = "{}://{}:{}@{}:{}/{}".format(db_config['db_sql_alchemy'],
                                               db_config['db_user'],
                                               db_config['db_pass'],
                                               db_config['db_host'],
                                               db_config['db_port'],
                                               db_config['db_name'])
            return uri

    def postgres_db(self, db=None, **kwargs):
        if db is None:
            db_conn = psycopg2.connect(database=kwargs['db_name'],
                                       user=kwargs['db_user'],
                                       password=kwargs['db_pass'],
                                       host=kwargs['db_host'],
                                       port=kwargs['db_port'])
            return db_conn
        opr_type = kwargs["opr_type"]
        sql = kwargs['sql']
        number_of_row = kwargs['number_of_row']
        cursor = db.cursor()
        if opr_type == "update" or opr_type == "update":
            cursor.execute(sql)
            db.commit()
            db.close()
            return True
        elif opr_type == "select":
            # print(kwargs['sql'])
            cursor.execute(sql)
            if number_of_row == 0:
                rows = cursor.fetchall()
                db.close()
                # print(rows)
                return rows
        else:
            return False

    def maria_db(self, db=None, **kwargs):
        try:
            # 连接MySQL数据库
            if db is None:
                db_conn = pymysql.connect(host=kwargs['db_host'],
                                          port=kwargs['db_port'],
                                          user=kwargs['db_user'],
                                          password=kwargs['db_pass'],
                                          db=kwargs['db_name'],
                                          charset=kwargs['db_char'],
                                          cursorclass=pymysql.cursors.DictCursor)
                return db_conn
            # print(db)
            sql = kwargs['sql']
            opr_type = kwargs['opr_type']
            number_of_row = kwargs['number_of_row']
            # 通过cursor创建游标
            db_cursor = db.cursor()
            if opr_type == "select":
                db_cursor.execute(sql)
                if number_of_row == 1:
                    raw_data = db_cursor.fetchone()
                    return raw_data
                if number_of_row > 0:
                    raw_data = db_cursor.fetchmany(number_of_row)
                    return raw_data
                else:
                    raw_data = db_cursor.fetchall()
                    return raw_data
            elif opr_type == "close":
                db.close()
                return True
            elif opr_type == "close_commit":
                db.commit()
                db.close()
                return True
            elif opr_type in ["update", "insert"]:
                db_cursor.execute(sql)
                db.commit()
                return True
            elif opr_type in ["update_nocommit", "insert_nocommit"]:
                db_cursor.execute(sql)
                return True
            else:
                return False
        except Exception as e:
            # return "conn_lost" anyway, and let db_entry() to retry 10 times
            err = "{},{}".format(__file__, e)
            logger_i("WARNING", err)
            return "conn_lost"

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

    def execute_bat(self, bat_file_path, bat_file):
        bat_file_path = os.path.join(bat_file_path, bat_file)
        exe_bat = subprocess.Popen("cmd.exe /c" + "%s abc" % bat_file_path, stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)
        cur_line = exe_bat.stdout.readline()
        while (cur_line != b''):
            # print(cur_line.decode('GBK'))
            cur_line = exe_bat.stdout.readline()
        exe_bat.wait()
        # print(execute_bat.returncode)
        exe_bat.terminate()

    def wcmd(self, command):
        excuet_bat = subprocess.Popen("cmd.exe /c" + "%s abc" % command, stdout=subprocess.PIPE,
                                      stderr=subprocess.STDOUT)
        cur_line = excuet_bat.stdout.readline()
        while (cur_line != b''):
            # print(cur_line.decode('GBK'))
            cur_line = excuet_bat.stdout.readline()
        excuet_bat.wait()
        # print(execute_bat.returncode)
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
