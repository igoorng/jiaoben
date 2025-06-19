import requests
import json
import schedule
import time
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def login_and_claim():
    # 第一个请求：用户登录
    login_url = "https://api.cross-play.xyz/users/login"
    login_headers = {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "content-type": "application/json",
        "origin": "https://app.cross-play.xyz",
        "priority": "u=1, i",
        "referer": "https://app.cross-play.xyz/",
        "sec-ch-ua": '"Microsoft Edge WebView2";v="137", "Microsoft Edge";v="137", "Not/A)Brand";v="24", "Chromium";v="137"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0"
    }
    login_data = {
        "encodedMessage": "user=%7B%22id%22%3A7081888702%2C%22first_name%22%3A%22one%22%2C%22last_name%22%3A%22van%F0%9F%90%9D%22%2C%22username%22%3A%22vantone_one%22%2C%22language_code%22%3A%22zh-hans%22%2C%22allows_write_to_pm%22%3Atrue%2C%22photo_url%22%3A%22https%3A%5C%2F%5C%2Ft.me%5C%2Fi%5C%2Fuserpic%5C%2F320%5C%2FnUatMG-I8Ng2ZcR4F_U71pyTnLnRgd773RPO9MXroq4Ai4nf-1bKNKLxfmYUv3wc.svg%22%7D&chat_instance=3307754930180099764&chat_type=private&start_param=A1yPzMJQ&auth_date=1750352769&signature=5o7NU1H57bmzt8dNnbWHo2htBRnX84zgh0DR6e-Q4SwmxtZQz0BpVnz0g-PZ4THV-gmfKYqd23lB0y-rmVrxBg&hash=bb3b5b2e43e419d016d840946a9b030d5bb7d7f2c8c0967574ace95f31f13c4e"
    }

    try:
        login_response = requests.post(login_url, headers=login_headers, json=login_data)
        login_response.raise_for_status()
        login_result = login_response.json()
        access_token = login_result.get("accessToken")
        logger.info("Login successful, access token: %s", access_token)
    except requests.exceptions.RequestException as e:
        logger.error("Login failed: %s", str(e))
        return

    # 第二个请求：领取金币
    claim_url = "https://api.cross-play.xyz/users/golds/claim"
    claim_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "authorization": f"Bearer {access_token}",
        "content-type": "application/json",
        "origin": "https://app.cross-play.xyz",
        "priority": "u=1, i",
        "referer": "https://app.cross-play.xyz/"
    }

    try:
        claim_response = requests.post(claim_url, headers=claim_headers)
        claim_response.raise_for_status()
        claim_result = claim_response.json()

        # 检查结果中是否包含webAppUserId
        if claim_result.get("user", {}).get("webAppUserId"):
            logger.info("Claim successful!")
            logger.info("Claim response: %s", json.dumps(claim_result, indent=2))
        else:
            logger.error("Claim failed: webAppUserId not found in response")
    except requests.exceptions.RequestException as e:
        logger.error("Claim failed: %s", str(e))

# 立即执行一次
login_and_claim()

# 每小时执行一次
schedule.every(1).hours.do(login_and_claim)

# 保持脚本运行
logger.info("Scheduler started, running every hour...")
while True:
    schedule.run_pending()
    time.sleep(60)  # 每分钟检查一次调度任务
