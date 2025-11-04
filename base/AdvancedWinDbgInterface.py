import subprocess
import threading
import time
import queue
import re
from base.helper import *
from base.contants import *

class AdvancedWinDbgInterface:
    def __init__(self, windbg_path="windbg.exe"):
        self.windbg_path = windbg_path
        self.process = None
        self.output_queue = queue.Queue()
        self.error_queue = queue.Queue()
        self.command_queue = queue.Queue()
        self.is_running = False
        self.output_callback = None
        self.error_callback = None
        self.command_list = []
        self.step_1_list = []
        self.step_2_list = []
        self.step_3_list = []
        self.step_4_list = []
        self.step_5_list = []
        self.step_6_list = []
        self.step_7_list = []
        self.step_8_list = []
        self.step_9_list = []
        self.step_10_list = []
        self.step_11_list = []
        self.step_12_list = []
        self.step_13_list = []
        self.step_14_list = []

        self.command_dict = {}

    def set_callbacks(self, output_callback=None, error_callback=None):
        """设置回调函数"""
        self.output_callback = output_callback
        self.error_callback = error_callback

    def start(self, target=None, args=None):
        """启动 WinDbg"""
        cmd_args = [self.windbg_path]
        if not os.path.exists(self.windbg_path):
            logger.info(f'{self.windbg_path} does not exist')

        if not os.path.exists(target):
            logger.info(f'{target} does not exist')
            return False

        if args:
            cmd_args.extend(args)

        if target:
            if isinstance(target, int):
                cmd_args.extend(["-p", str(target)])  # 附加到进程
            else:
                # "-y", f'{SYMBOL_PATH}',
                cmd_args.extend(["-z", target,
                                 "-c",".logopen tmp.log",
                                 "-y", f'{SYMBOL_PATH}',
                                 ])  # 打开转储文件

        try:
            self.process = subprocess.Popen(
                cmd_args,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=0,
                encoding="utf-8",
                errors='ignore',
                universal_newlines=True
            )

            self.is_running = True

            # 启动处理线程
            threading.Thread(target=self._handle_stdout, daemon=True).start()
            threading.Thread(target=self._handle_stderr, daemon=True).start()
            threading.Thread(target=self._handle_commands, daemon=True).start()

            # time_sleep = 45
            time_sleep = 15
            logger.info(f"WinDbg started successfully, time.sleep({time_sleep}) for loading")
            time.sleep(time_sleep)
            return True

        except Exception as e:
            logger.info(f"Failed to start WinDbg: {e}")
            return False

    def _handle_stdout(self):
        """处理标准输出"""
        while self.is_running and self.process:
            try:
                line = self.process.stdout.readline()
                if line:
                    self.output_queue.put(line.strip())
                    if self.output_callback:
                        self.output_callback(line.strip())
            except Exception as e:
                if self.is_running:
                    logger.info(f"Error reading stdout: {e}")
                break

    def _handle_stderr(self):
        """处理标准错误"""
        while self.is_running and self.process:
            try:
                line = self.process.stderr.readline()
                if line:
                    self.error_queue.put(line.strip())
                    if self.error_callback:
                        self.error_callback(line.strip())
            except Exception as e:
                if self.is_running:
                    logger.info(f"Error reading stderr: {e}")
                break

    def _handle_commands(self):
        """处理命令队列"""
        while self.is_running:
            try:
                if not self.command_queue.empty():
                    command = self.command_queue.get(timeout=0.1)
                    self._send_command_internal(command)
            except queue.Empty:
                continue
            except Exception as e:
                logger.info(f"Error handling commands: {e}")

    def _send_command_internal(self, command):
        """内部发送命令方法"""
        try:
            self.process.stdin.write(command + '\n')
            self.process.stdin.flush()
        except Exception as e:
            logger.info(f"Failed to send command '{command}': {e}")

    def send_command(self, command, async_send=True):
        """发送命令"""
        if not self.is_running or not self.process:
            raise Exception("WinDbg is not running")

        if async_send:
            self.command_queue.put(command)
        else:
            self._send_command_internal(command)

    def get_output(self, timeout=5):
        """获取输出"""
        lines = []
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                line = self.output_queue.get(timeout=0.1)
                lines.append(line)
            except queue.Empty:
                break

        return '\n'.join(lines)

    def get_error(self, timeout=5):
        """获取错误输出"""
        lines = []
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                line = self.error_queue.get(timeout=0.1)
                lines.append(line)
            except queue.Empty:
                break

        return '\n'.join(lines)


    def execute_command(self, command, current_step, timeout=10):
        if current_step:
            step_list_append = f'self.step_{current_step}_list.append(command)'
            eval(step_list_append)

            step_list = f'self.step_{current_step}_list'
            # logger.info(f"Command list: {eval(step_list)}")
            # self.step_list.append(command)

        # 清空现有输出
        while not self.output_queue.empty():
            try:
                self.output_queue.get_nowait()
            except queue.Empty:
                break

        # 发送命令
        self.send_command(command)

        sleep_time = 5
        for key, value in command_sleep_map.items():
            if key in command:
                sleep_time = value

        time.sleep(sleep_time)

        # 获取输出
        result = self.get_output(timeout)
        error = self.get_error(1)

        self.command_dict[command] = result
        if error:
            logger.info(f"Command error: {error}")

        return result

    def stop(self, dump_path):
        """停止 WinDbg"""
        cmd = ".logclose"
        logger.info(f'cmd: {cmd}')
        result = self.execute_command(cmd, current_step=None, timeout=15)
        step_dict = {}
        for idx in range(1, 15, 1):
            # logger.info(f"idx: {idx}")
            step = f'self.step_{idx}_list'
            if eval(step):
                step_dict[f'step_{idx}_list'] = eval(step)

        # command
        result_yaml_file = 'step_command.yaml'
        result_yaml_file = os.path.join(dump_path, result_yaml_file)
        fileOP.dump_file(result_yaml_file, step_dict)

        # command
        result_yaml_file = 'command_dict.yaml'
        result_yaml_file = os.path.join(dump_path, result_yaml_file)
        fileOP.dump_file(result_yaml_file, self.command_dict)

        self.is_running = False

        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()

# 使用示例
def output_handler(line):
    logger.info(f"[WinDbg Output] {line}")


def error_handler(line):
    logger.info(f"[WinDbg Error] {line}")

def windbg_cmd(dump_file, commands):
    # # 创建高级接口
    # windbg = AdvancedWinDbgInterface(
    #     r"C:\Users\15319\AppData\Local\Microsoft\WindowsApps\kdX86.exe"
    # )

    # 设置回调
    windbg.set_callbacks(output_handler, error_handler)

    # 启动 WinDbg
    if windbg.start(target=dump_file):
        # time.sleep(3)  # 等待初始化
        for cmd in commands:
            logger.info(f"Executing: {cmd}")
            cmd_output = windbg.execute_command(cmd, current_step, timeout=15)
            if result:
                logger.info(f"Result:\n{result}")
            logger.info("-" * 50)
            # time.sleep(1)

        # 保持运行
        try:
            time.sleep(5)
        except KeyboardInterrupt:
            logger.info("Stopping...")

        windbg.stop(path_dir)
    return

# kdX86_path = r"C:\Users\15319\AppData\Local\Microsoft\WindowsApps\kdX86.exe"
windbg = AdvancedWinDbgInterface(
    kdX86_path
)

if __name__ == "__main__":
    logger.info('hello')
    dump_file = r"D:\0_LOG_VIP\11\0x9f_3_Disk_FastBoot\MEMORY.DMP"
    # 执行一些调试命令
    commands = [
        "!analyze  -v",
        ".logclose",
        "q"
    ]
    windbg_cmd(dump_file, commands)
