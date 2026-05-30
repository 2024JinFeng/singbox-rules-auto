import os
import json
import subprocess
import shutil
import requests

# 严格使用你给的原始链接，不做任何自作聪明的二次修改
TASKS = {
    "ChatGPT": [
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/OpenAI/OpenAI.list"
    ],
    "Other Ai": [
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/Copilot/Copilot.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/Gemini/Gemini.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/Claude/Claude.list",
        "https://raw.githubusercontent.com/liandu2024/clash/refs/heads/main/list/MetaAi.list",
        "https://raw.githubusercontent.com/liandu2024/clash/refs/heads/main/list/Perplexity.list"
    ],
    "GitHub": ["https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/GitHub/GitHub.list"],
    "TikTok": ["https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/TikTok/TikTok.list"],
    "Instagram": ["https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/Instagram/Instagram.list"],
    "Telegram": ["https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/Telegram/Telegram.list"],
    "Twitter_FB_WA": [
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/Twitter/Twitter.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/Facebook/Facebook.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/Whatsapp/Whatsapp.list"
    ],
    "Steam": ["https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/Steam/Steam.list"],
    "Game": [
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/Epic/Epic.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/EA/EA.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/Blizzard/Blizzard.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/UBI/UBI.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/Sony/Sony.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/Nintendo/Nintendo.list"
    ],
    "YouTube": ["https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/YouTube/YouTube.list"],
    "Disney": ["https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/Disney/Disney.list"],
    "Netflix": ["https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/Netflix/Netflix.list"],
    "Spotify": ["https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/Spotify/Spotify.list"],
    "Amazon": ["https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/Amazon/Amazon.list"],
    "Apple": ["https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/Apple/Apple.list"],
    "Microsoft": ["https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/Microsoft/Microsoft.list"],
    "Google": ["https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/Google/Google.list"],
    "TEST": ["https://raw.githubusercontent.com/liandu2024/clash/refs/heads/main/list/Check.list"],
    "Block": [
        "https://raw.githubusercontent.com/liandu2024/clash/refs/heads/main/list/Block.list",
        "https://raw.githubusercontent.com/peiyingyao/Rule-for-OCD/refs/heads/master/rule/Clash/BlockHttpDNS/BlockHttpDNS.list"
    ],
    "Emby-Proxy": ["https://raw.githubusercontent.com/2024JinFeng/clash/refs/heads/main/Emby-Proxy.list"],
    "Emby-Direct": ["https://raw.githubusercontent.com/2024JinFeng/clash/refs/heads/main/Emby-Direct.list"],
    "Direct": [
        "https://raw.githubusercontent.com/peiyingyao/Rule-for-OCD/refs/heads/master/rule/Clash/Proxy/Proxy.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/ChinaMax/ChinaMax.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/China/China.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/PrivateTracker/PrivateTracker.list"
    ],
    "Proxy": [
        "https://raw.githubusercontent.com/peiyingyao/Rule-for-OCD/refs/heads/master/rule/Clash/Proxy/Proxy.list",
        "https://raw.githubusercontent.com/peiyingyao/Rule-for-OCD/refs/heads/master/rule/Clash/Global/Global.list"
    ],
    "AMD": ["https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/AMD/AMD.list"],
    "Nvidia": ["https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/Clash/Nvidia/Nvidia.list"]
}

SRS_OUTPUT_DIR = "srs"

def compile_to_srs(json_path, rule_name):
    singbox_bin = "./sing-box" if os.path.exists("./sing-box") else shutil.which("sing-box")
    if not singbox_bin:
        print(f"⚠️ 未找到 sing-box 编译器")
        return False
    os.makedirs(SRS_OUTPUT_DIR, exist_ok=True)
    srs_path = os.path.join(SRS_OUTPUT_DIR, f"{rule_name}.srs")
    cmd = [singbox_bin, "rule-set", "compile", json_path, "-o", srs_path]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        print(f"🟢 编译成功: {srs_path}")
        if os.path.exists(json_path):
            os.remove(json_path)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 编译失败 {rule_name}: {e.stderr.decode().strip()}")
        return False

def process_convert():
    for rule_name, urls in TASKS.items():
        result = {"version": 1, "rules": [{"domain": [], "domain_suffix": [], "domain_keyword": [], "ip_cidr": [], "ip_asn": []}]}
        rule = result["rules"][0]
        has_data = False # 新增：标记是否成功下载到数据

        for url in urls:
            try:
                # 🔴 核心修复：移除对 url 字符串的二次替换，直接使用你的原链接请求
                resp = requests.get(url, timeout=15)
                resp.raise_for_status()
                resp.encoding = 'utf-8'
                
                lines = resp.text.splitlines()
                for line in lines:
                    line = line.strip()
                    if not line or line.startswith(("#", "payload:")): continue
                    if line.startswith("- "): line = line[2:]
                    parts = line.split(",")
                    if len(parts) < 2: continue
                    t, v = parts[0].strip().upper(), parts[1].strip()
                    if t == "DOMAIN": rule["domain"].append(v.lower())
                    elif t == "DOMAIN-SUFFIX": rule["domain_suffix"].append(v.lower())
                    elif t == "DOMAIN-KEYWORD": rule["domain_keyword"].append(v.lower())
                    elif t in ["IP-CIDR", "IP-CIDR6"]: rule["ip_cidr"].append(v)
                    elif t == "IP-ASN": rule["ip_asn"].append(str(v))
                has_data = True
            except Exception as e:
                print(f"⚠️ 链接抓取失败: {url} | 原因: {e}")
                continue

        # 只有在成功抓取到数据时才进行转换，避免空规则报错
        if has_data:
            for key in list(rule.keys()):
                if rule[key]: rule[key] = sorted(list(set(rule[key])))
                else: del rule[key]
            
            temp_json_path = f"temp_{rule_name}.json"
            with open(temp_json_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            compile_to_srs(temp_json_path, rule_name)
        else:
            print(f"❌ 分类 {rule_name} 下的所有链接均无法获取有效数据，跳过编译。")

if __name__ == "__main__":
    process_convert()
