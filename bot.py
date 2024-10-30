import requests
import json
import os
import urllib.parse
import hashlib
from colorama import *
from datetime import datetime
import time
import pytz

wib = pytz.timezone('Asia/Jakarta')

class FreeDOGS:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'no-cache',
            'Host': 'api.freedogs.bot',
            'Origin': 'https://app.freedogs.bot',
            'Pragma': 'no-cache',
            'Referer': 'https://app.freedogs.bot/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'
        }

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def log(self, message):
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{message}",
            flush=True
        )

    def welcome(self):
        print(
            f"""
        {Fore.GREEN + Style.BRIGHT}Auto Claim {Fore.BLUE + Style.BRIGHT}Free DOGS - BOT
            """
            f"""
        {Fore.GREEN + Style.BRIGHT}Rey? {Fore.YELLOW + Style.BRIGHT}<INI WATERMARK>
            """
        )

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

    def extract_user_data(self, query: str) -> str:
        user_data_encoded = query.split('user%3D')[1].split('%26')[0]

        if user_data_encoded:
            user_data = urllib.parse.unquote(urllib.parse.unquote(user_data_encoded))
            user_json = json.loads(user_data)
            return str(user_json.get('first_name', 'Unknown'))
        return 'Unknown'


    def load_tokens(self):
        try:
            if not os.path.exists('tokens.json'):
                return {"accounts": []}

            with open('tokens.json', 'r') as file:
                data = json.load(file)
                if "accounts" not in data:
                    return {"accounts": []}
                return data
        except json.JSONDecodeError:
            return {"accounts": []}

    def save_tokens(self, tokens):
        with open('tokens.json', 'w') as file:
            json.dump(tokens, file, indent=4)

    def generate_tokens(self, queries: list):
        tokens_data = self.load_tokens()
        accounts = tokens_data["accounts"]

        for idx, query in enumerate(queries):
            account_name = self.extract_user_data(query)

            existing_account = next((acc for acc in accounts if acc["first_name"] == account_name), None)

            if not existing_account:
                print(
                    f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} {account_name} {Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT}Token Is None{Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT} ] [{Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT} Generating Token... {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}",
                    end="\r", flush=True
                )
                time.sleep(1)

                token = self.get_token(query)
                if token:
                    self.log(
                        f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} {account_name} {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}] [{Style.RESET_ALL}"
                        f"{Fore.GREEN + Style.BRIGHT} Successfully Generated Token {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}                           "
                    )
                    accounts.insert(idx, {"first_name": account_name, "token": token})
                else:
                    self.log(
                        f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} {account_name} {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}] [{Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT} Failed to Generate Token {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}                           "
                    )

                time.sleep(1)
                self.log(f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}" * 75)

        self.save_tokens({"accounts": accounts})

    def renew_token(self, account_name):
        tokens_data = self.load_tokens()
        accounts = tokens_data.get("accounts", [])
        
        account = next((acc for acc in accounts if acc["first_name"] == account_name), None)
        
        if account and "token" in account:
            token = account["token"]
            if not self.mine_info(token):
                print(
                    f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} {account_name} {Style.RESET_ALL}"
                    f"{Fore.RED + Style.BRIGHT}Token Isn't Valid{Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT} ] [{Style.RESET_ALL}"
                    f"{Fore.YELLOW + Style.BRIGHT} Regenerating Token... {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}",
                    end="\r", flush=True
                )
                time.sleep(1)
                
                accounts = [acc for acc in accounts if acc["first_name"] != account_name]
                
                query = next((query for query in self.load_queries() if self.extract_user_data(query) == account_name), None)
                if query:
                    new_token = self.get_token(query)
                    if new_token:
                        accounts.append({"first_name": account_name, "token": new_token})
                        self.log(
                            f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} {account_name} {Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT}] [{Style.RESET_ALL}"
                            f"{Fore.GREEN + Style.BRIGHT} Successfully Generated Token {Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}                           "
                        )
                    else:
                        self.log(
                            f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT} {account_name} {Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT}] [{Style.RESET_ALL}"
                            f"{Fore.RED + Style.BRIGHT} Failed to Generate Token {Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}                           "
                        )
                else:
                    self.log(
                        f"{Fore.MAGENTA + Style.BRIGHT}[ Account{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} {account_name} {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}] [{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Query Is None. Skipping {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}                           "
                    )

                time.sleep(1)
        
        self.save_tokens({"accounts": accounts})

    def load_queries(self):
        with open('query.txt', 'r') as file:
            return [line.strip() for line in file if line.strip()]
        
    def get_token(self, query: str):
        url = f"https://api.freedogs.bot/miniapps/api/user/telegram_auth?invitationCode=Yum5S6tN&initData={query}"
        data = json.dumps({'invitationCode':'Yum5S6tN', 'initData':query})
        self.headers.update({
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        })

        response = self.session.post(url, headers=self.headers, data=data, allow_redirects=True)
        response.raise_for_status()
        result = response.json()
        if result['code'] == 0:
            return result['data']['token']
        else:
            return None
        
    def mine_info(self, token: str):
        url = 'https://api.freedogs.bot/miniapps/api/mine/getMineInfo?'
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        })

        response = self.session.get(url, headers=self.headers, allow_redirects=True)
        response.raise_for_status()
        result = response.json()
        if result['code'] == 0:
            return result['data']
        else:
            return False
        
    def game_info(self, token: str):
        url = 'https://api.freedogs.bot/miniapps/api/user_game_level/GetGameInfo?'
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        })

        response = self.session.get(url, headers=self.headers, allow_redirects=True)
        response.raise_for_status()
        result = response.json()
        if result['code'] == 0:
            return result['data']
        else:
            return None
    
    def generate_hash(self, amount: str, seq_no: str):
        static_string = "7be2a16a82054ee58398c5edb7ac4a5a"
        combined = str(amount) + str(seq_no) + static_string
        return hashlib.md5(combined.encode()).hexdigest()

    def collect_coin(self, token: str, amount: str, hash_code: str, seq_no: str):
        url = "https://api.freedogs.bot/miniapps/api/user_game/collectCoin?"
        data = {'collectAmount': amount, 'hashCode': hash_code, 'collectSeqNo': seq_no}
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        })

        response = self.session.post(url, headers=self.headers, data=data, allow_redirects=True)
        response.raise_for_status()
        result = response.json()
        if result['code'] == 0:
            return result['data']
        else:
            return None
        
    def tasks_list(self, token: str):
        url = 'https://api.freedogs.bot/miniapps/api/task/lists?'
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        })

        response = self.session.get(url, headers=self.headers, allow_redirects=True)
        response.raise_for_status()
        result = response.json()
        if result['code'] == 0:
            return result['data']['lists']
        else:
            return None
        
    def finish_tasks(self, token: str, task_id: str):
        url = f'https://api.freedogs.bot/miniapps/api/task/finish_task?id={task_id}'
        data = json.dumps({'id': task_id})
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        })

        response = self.session.post(url, headers=self.headers, data=data)
        response.raise_for_status()
        result = response.json()
        if result['code'] == 0:
            return result
        else:
            return None
    
    def process_query(self, query: str):
        account_name = self.extract_user_data(query)
    
        tokens_data = self.load_tokens()
        accounts = tokens_data.get("accounts", [])

        exist_account = next((acc for acc in accounts if acc["first_name"] == account_name), None)
        
        if exist_account and "token" in exist_account:
            token = exist_account["token"]

            mine_info = self.mine_info(token)
            if not mine_info:
                self.renew_token(account_name)
                tokens_data = self.load_tokens()
                new_account = next((acc for acc in tokens_data["accounts"] if acc["first_name"] == account_name), None)
                
                if new_account and "token" in new_account:
                    new_token = new_account["token"] 
                    mine_info = self.mine_info(new_token)

            if mine_info:
                self.log(
                    f"{Fore.MAGENTA+Style.BRIGHT}[ Account{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {account_name} {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}] [ Balance{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {mine_info['getCoin']} {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                )

                game = self.game_info(new_token if 'new_token' in locals() else token)
                if game:
                    max_click = game['userToDayMaxClick']
                    today_click = game['userToDayNowClick']
                    amount = int(game['coinPoolLeft'])
                    seq_no = int(game['collectSeqNo'])
                    hash_code = self.generate_hash(amount, seq_no)

                    if today_click < max_click:
                        collect = self.collect_coin(new_token if 'new_token' in locals() else token, amount, hash_code, seq_no)
                        if collect:
                            self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT}[ Tap Tap{Style.RESET_ALL}"
                                f"{Fore.GREEN+Style.BRIGHT} is Completed {Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT}] [ Reward{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} {collect['collectAmount']} {Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                            )
                        else:
                            self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT}[ Tap Tap{Style.RESET_ALL}"
                                f"{Fore.RED+Style.BRIGHT} is Failed {Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                            )
                    else:
                        self.log(f"{Fore.YELLOW + Style.BRIGHT}[ Tap Tap Reached Maximum Limit ]{Style.RESET_ALL}")
                else:
                    self.log(f"{Fore.RED+Style.BRIGHT}[ Error Fetching Game Info ]{Style.RESET_ALL}")

                tasks = self.tasks_list(new_token if 'new_token' in locals() else token)
                completed_tasks = False
                if tasks:
                    for task in tasks:

                        if task['isFinish'] == 0:
                            task_id = task['id']

                            finish = self.finish_tasks(new_token if 'new_token' in locals() else token, task_id)
                            if finish:
                                self.log(
                                    f"{Fore.MAGENTA+Style.BRIGHT}[ Task{Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT} {task['name']} {Style.RESET_ALL}"
                                    f"{Fore.GREEN+Style.BRIGHT} is Completed {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT}] [ Reward{Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT} {task['rewardParty']} {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                                )
                            else:
                                self.log(
                                    f"{Fore.MAGENTA+Style.BRIGHT}[ Task{Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT} {task['name']} {Style.RESET_ALL}"
                                    f"{Fore.RED+Style.BRIGHT} is Failed {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                                )
                        else:
                            completed_tasks = True

                    if completed_tasks:
                        self.log(f"{Fore.YELLOW+Style.BRIGHT}[ All Available Task is Completed ]{Style.RESET_ALL}")
                else:
                    self.log(f"{Fore.RED+Style.BRIGHT}[ Error Fetching Tasks Info ]{Style.RESET_ALL}")
        
    def main(self):
        self.clear_terminal()
        try:
            queries = self.load_queries()
            self.generate_tokens(queries)

            while True:
                self.clear_terminal()
                self.welcome()
                self.log(
                    f"{Fore.GREEN + Style.BRIGHT}Account's Total: {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{len(queries)}{Style.RESET_ALL}"
                )
                self.log(f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}"*75)

                for query in queries:
                    if query:
                        self.process_query(query)
                        self.log(f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}"*75)

                seconds = 180
                while seconds > 0:
                    formatted_time = self.format_seconds(seconds)
                    print(
                        f"{Fore.CYAN+Style.BRIGHT}[ Wait for{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {formatted_time} {Style.RESET_ALL}"
                        f"{Fore.CYAN+Style.BRIGHT}... ]{Style.RESET_ALL}",
                        end="\r"
                    )
                    time.sleep(1)
                    seconds -= 1

        except KeyboardInterrupt:
            self.log(f"{Fore.RED + Style.BRIGHT}[ EXIT ] Free DOGS - BOT{Style.RESET_ALL}")
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}An error occurred: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    freedogs = FreeDOGS()
    freedogs.main()