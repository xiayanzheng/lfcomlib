from lfcomlib.Jessica import requests, os, time, sqlite3, subprocess, configparser, codecs, parse, Msg
from lfcomlib.Jessica import shutil, telnetlib
from lfcomlib.Jessica.Err import logger_i
from lfcomlib.Jessica import uuid
from lfcomlib.Jessica import DaPrCore

DaPr = DaPrCore.Core()


class Infra:

    def __init__(self):
        self.db_opr_type = {
            "close": "close",
            "insert": "insert",
            "commit": "commit",
            "update": "update",
            "select": "select"
        }
        self.db_cfg_save = None
        self.db_instance = None
        self.db_controller = None
        self.db_connect_error = None
        self.log_cfg = {}

    def get_mac_address(self):
        mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
        return ":".join([mac[e:e + 2] for e in range(0, 11, 2)])

    def rename_ff(self, from_, to_, show_msg=True):
        obj = from_
        if os.path.isdir(obj):
            try:
                os.rename(obj, to_)
            finally:
                pass
            if show_msg:
                print("Folder {} renamed to {}".format(obj, to_))
        if os.path.isfile(obj):
            os.rename(obj, to_)
            if show_msg:
                print("File {} renamed to {}".format(obj, to_))

    def remove_ff(self, ff, show_msg=True):
        if os.path.exists(ff):
            if os.path.isdir(ff):
                shutil.rmtree(ff)
                if show_msg:
                    print("Folder {} deleted".format(ff))
            else:
                os.remove(ff)
                if show_msg:
                    print("File {} deleted".format(ff))
        else:
            if show_msg:
                print("Delete Operation Filed".format(ff))
            return False

    def dir_check(self, u_dir):
        if not os.path.exists(u_dir):
            os.makedirs(u_dir)
            return u_dir
        else:
            return u_dir

    def move_ff(self, from_, to_, show_msg=True):
        shutil.move(from_, to_)

    def get_folder_size(self, folder):
        folder_size = 0
        for Root, Dirs, Files in os.walk(folder):
            for File in Files:
                folder_size += os.path.getsize(os.path.join(Root, File))
        return folder_size

    def copy_ff(self, from_, to_, show_msg=True):
        _from = from_
        _to = to_
        if os.path.isdir(from_):
            _to = os.path.join(to_, os.path.basename(from_))
            if not os.path.exists(_to):
                shutil.copytree(from_, _to)
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
            print("From:", _from)
            print("To:", _to)
            print("File {} Copied".format(_from))
            print("++++++++++++++++")

    def copy_ff_with_del(self, from_, to_, show_msg=True):
        if os.path.exists(to_):
            if os.path.isdir(to_):
                shutil.rmtree(to_)
            else:
                os.remove(to_)
        self.copy_ff(from_, to_, show_msg)

    def open_dir(self, selected_dir):
        os.system("explorer %s" % DaPr.replace_dir_slash(selected_dir))

    def open_file(self, program, selected_dir, param):
        if param is None:
            param_x = ' '
        else:
            param_x = param
        os.system("{} {} {}".format(program, DaPr.replace_dir_slash(selected_dir), param_x))

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

    def db_commit(self):
        sql_commit_cfg = {
            'sql': '',
            'opr_type': 'commit',
            'number_of_row': 0
        }
        return self.db_entry(**sql_commit_cfg)

    def db_init(self, db_type=None, **kwargs):
        from lfcomlib.Jessica import pymysql, psycopg2
        retry_count = 0
        if db_type in ["maria", "mysql"]:
            self.db_controller = self.maria_db
            self.db_connect_error = (pymysql.OperationalError, pymysql.InterfaceError)
        elif db_type == "postgres":
            self.db_controller = self.postgres_db
            self.db_connect_error = (psycopg2.OperationalError, psycopg2.InterfaceError)
        else:
            return False

        if self.db_instance is None:
            self.db_cfg_save = kwargs
            self.db_instance = self.db_controller(db_open=True, **kwargs)
        return True

    def db_entry(self, **kwargs):
        retry_count = 0
        while True:
            try:
                return self.db_controller(db_open=False, **kwargs)
            except self.db_connect_error:
                if retry_count >= 3:
                    print("retry over to connect DB")
                    return False
                else:
                    retry_count += 1
                    print("DB connection lost")
                    time.sleep(1)
                    self.db_instance = self.db_controller(db_open=True, **self.db_cfg_save)
                    continue
            except Exception:
                return False

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

    def postgres_db(self, db_open=False, **kwargs):
        from lfcomlib.Jessica import psycopg2, psycopg2_extras
        try:
            # 连接MySQL数据库
            if db_open is True:
                db_conn = psycopg2.connect(database=kwargs['db_name'],
                                           user=kwargs['db_user'],
                                           password=kwargs['db_pass'],
                                           host=kwargs['db_host'],
                                           port=kwargs['db_port'])
                return db_conn

            sql = kwargs['sql']
            opr_type = kwargs['opr_type']
            number_of_row = kwargs['number_of_row']

            # 通过cursor创建游标
            if opr_type == "select":
                db_cursor = self.db_instance.cursor(cursor_factory=psycopg2_extras.RealDictCursor)
                db_cursor.execute(sql)
                if number_of_row == 1:
                    raw_data = db_cursor.fetchone()
                elif number_of_row > 0:
                    raw_data = db_cursor.fetchmany(number_of_row)
                else:
                    raw_data = db_cursor.fetchall()
                db_cursor.close()
                return raw_data
            elif opr_type == "close":
                self.db_instance.close()
                self.db_instance = None
                return True
            elif opr_type == "commit":
                self.db_instance.commit()
                return True
            elif opr_type in ["update_nocommit", "insert_nocommit"]:
                db_cursor = self.db_instance.cursor(cursor_factory=psycopg2_extras.RealDictCursor)
                db_cursor.execute(sql)
                db_cursor.close()
                return True
            else:
                return False
        except Exception as e:
            err = "{},{}".format(os.path.basename(__file__), e)
            logger_i("ERROR", err)
            raise

    def maria_db(self, db_open=False, **kwargs):
        from lfcomlib.Jessica import pymysql
        try:
            # 连接MySQL数据库
            if db_open is True:
                db_conn = pymysql.connect(host=kwargs['db_host'],
                                          port=kwargs['db_port'],
                                          user=kwargs['db_user'],
                                          password=kwargs['db_pass'],
                                          db=kwargs['db_name'],
                                          charset=kwargs['db_char'],
                                          cursorclass=pymysql.cursors.DictCursor)
                return db_conn

            sql = kwargs['sql']
            opr_type = kwargs['opr_type']
            number_of_row = kwargs['number_of_row']

            # 通过cursor创建游标
            if opr_type == "select":
                db_cursor = self.db_instance.cursor()
                db_cursor.execute(sql)
                if number_of_row == 1:
                    raw_data = db_cursor.fetchone()
                elif number_of_row > 0:
                    raw_data = db_cursor.fetchmany(number_of_row)
                else:
                    raw_data = db_cursor.fetchall()
                db_cursor.close()
                return raw_data
            elif opr_type == "close":
                self.db_instance.close()
                self.db_instance = None
                return True
            elif opr_type == "commit":
                self.db_instance.commit()
                return True
            elif opr_type in ["update_nocommit", "insert_nocommit"]:
                db_cursor = self.db_instance.cursor()
                db_cursor.execute(sql)
                db_cursor.close()
                return True
            else:
                return False
        except Exception as e:
            err = "{},{}".format(os.path.basename(__file__), e)
            logger_i("ERROR", err)
            raise

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
                    return DaPr.merge_multi_tuple_list(object, raw_data)
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
                return DaPr.merge_multi_tuple_list(raw_data)
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

    def cmd_con_lite(self, command, return_mode="list"):
        if type(command) is list:
            cmd = os.popen(command)
        else:
            cmd = os.popen(str(command))
        output = cmd.read()
        if return_mode == 'list':
            output = output.split('\n')
        cmd.close()
        return output

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


class TelnetConn:

    def __init__(self):
        self.tn = None
        self.buffer = []
        self.debug = False

    def create_telnet_session(self, host, port=23):
        self.tn = telnetlib.Telnet(host, port)

    def telnet_interface(self, show_response=False, **kwargs):
        cfg = kwargs
        if cfg['execute_type'] == 'direct':
            self.run_direct(show_response, **cfg)
        if cfg['execute_type'] == 'loop':
            self.run_loop(show_response, **cfg)

    def run_direct(self, show_response=False, **kwargs):
        cfg = kwargs
        # print("[Execute Type:{}][Task Name:{}]".format(cfg['execute_type'], cfg['command_name']))
        rsp = str(cfg['response']).encode('ascii') + b"\n"
        if type(cfg['expect']) is list:
            for exp_i in cfg['expect']:
                print(exp_i)
                response = self.tn.read_very_eager().decode('ascii')
                print("{}--------{}".format(str(exp_i), str(response)))
                print("sse", response)
                if exp_i in response:
                    response = self.tn.read_until(bytes(exp_i, encoding="utf8"), timeout=cfg["timeout"]).decode('ascii')
                    print(type(exp_i), type(response))
                    print("rereer", exp_i, "+++", response, "+++", exp_i in response)
                    print("rep{}".format(response))

        else:
            # exp = bytes(cfg['expect'], encoding="utf8")
            exp = cfg['expect']
            print(exp)
            if cfg['expect'] != "":
                response = self.tn.read_until(bytes(exp, encoding="utf8"), timeout=cfg["timeout"]).decode('ascii')
                print(type(exp), type(response))
                print("rear", exp, "+++", response, "+++", exp in response)
                print("rep{}".format(response))
        self.tn.write(rsp)
        time.sleep(cfg['time_wait'])
        temp = self.tn.read_very_eager().decode('ascii')
        print("temp{}".format(temp))
        self.buffer.append(temp)
        print(self.buffer)
        if show_response:
            print("Telnet response start")
            print(temp)
            print("Telnet response end")
            input("Continue:")

    def run_loop(self, show_response, **kwargs):
        cfg = kwargs
        loop_time = cfg['loop_time']
        for i in range(loop_time):
            self.run_direct(show_response, **cfg)
