import os
import json
import subprocess
import shutil
import requests

# 严格使用你给的原始链接
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
    singbox_bin = (
        "./sing-box"
        if os.path.exists("./sing-box")
        else shutil.which("sing-box")
    )
    if not singbox_bin:
        print("未找到 sing-box")
        return False

    os.makedirs(SRS_OUTPUT_DIR, exist_ok=True)
    srs_path = os.path.join(SRS_OUTPUT_DIR, f"{rule_name}.srs")
    cmd = [singbox_bin, "rule-set", "compile", json_path, "-o", srs_path]

    print("\n===================")
    print("编译:", rule_name)
    print("JSON:", json_path)

    result = subprocess.run(cmd, capture_output=True, text=True)
    print("stdout:", result.stdout)
    print("stderr:", result.stderr)

    if result.returncode == 0:
        print(f"编译成功: {srs_path}")
        if os.path.exists(json_path):
            os.remove(json_path)
        return True
    else:
        print(f"编译失败: {rule_name}")
        return False

def process_convert():
    for rule_name, urls in TASKS.items():
        # 严格控制初始化结构，绝不携带任何包含 asn/ip_asn 的键值
        result = {
            "version": 1,
            "rules": [
                {
                    "domain": [],
                    "domain_suffix": [],
                    "domain_keyword": [],
                    "ip_cidr": []
                }
            ]
        }
        rule = result["rules"][0]

        for url in urls:
            try:
                print(f"\n下载: {url}")
                resp = requests.get(url, timeout=30)
                resp.raise_for_status()
                resp.encoding = "utf-8"

                for line in resp.text.splitlines():
                    line = line.strip()
                    if not line or line.startswith("#") or line.startswith("payload:"):
                        continue
                    if line.startswith("- "):
                        line = line[2:]

                    parts = line.split(",", 1)
                    if len(parts) < 2:
                        continue

                    rule_type = parts[0].strip().upper()
                    value = parts[1].strip()

                    # 彻底过滤并阻断所有 ASN 规则类型
                    if rule_type in ("IP-ASN", "ASN"):
                        continue

                    # 清洗并切断 Clash 规则中 IP 后缀常带的 ,no-resolve 小尾巴
                    if ",no-resolve" in value.lower():
                        value = value.lower().split(",no-resolve")[0].strip()

                    if rule_type == "DOMAIN":
                        rule["domain"].append(value.lower())
                    elif rule_type == "DOMAIN-SUFFIX":
                        rule["domain_suffix"].append(value.lower())
                    elif rule_type == "DOMAIN-KEYWORD":
                        rule["domain_keyword"].append(value.lower())
                    elif rule_type in ("IP-CIDR", "IP-CIDR6"):
                        rule["ip_cidr"].append(value)

            except Exception as e:
                print(f"抓取失败: {url} | 错误: {e}")

        # 去重排序
        for key in list(rule.keys()):
            if rule[key]:
                rule[key] = sorted(set(rule[key]))
            else:
                del rule[key]

        # 细分数据条数打印（用于核对 Direct 等分类是否条数异常）
        print(
            f"📊 {rule_name} 细分统计 -> "
            f"DOMAIN: {len(rule.get('domain', []))} | "
            f"SUFFIX: {len(rule.get('domain_suffix', []))} | "
            f"KEYWORD: {len(rule.get('domain_keyword', []))} | "
            f"IP_CIDR: {len(rule.get('ip_cidr', []))}"
        )

        total_rules = 0
        for v in rule.values():
            total_rules += len(v)

        if total_rules == 0:
            print(f"跳过空规则集: {rule_name}")
            continue

        temp_json_path = f"temp_{rule_name.replace(' ','_')}.json"
        with open(temp_json_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        # 现场照妖镜：打印写入的 JSON 前 300 字符，用于自证完全没有 asn 污染
        print(f"🔍 已生成 {temp_json_path}，实际内容前缀验证:")
        with open(temp_json_path, "r", encoding="utf-8") as f:
            print(f.read(300))

        compile_to_srs(temp_json_path, rule_name.replace(" ", "_"))

if __name__ == "__main__":
    process_convert()
