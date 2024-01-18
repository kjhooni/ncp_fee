from datetime import datetime
import time

space = " "
new_line = "\n"
date = datetime.now()
today_date = date.strftime("%Y-%m-%d")
yyyymm = date.strftime("%Y%m")
mm = date.month

timestamp = int(time.time() * 1000)
timestamp = str(timestamp)
print(timestamp)
apicall_method_get = "GET"
apicall_method_post = "POST"

getproductde = "getProductDemandCostListResponse"
productde = "productDemandCostList"
uA = "useAmount"

gov_billing_api_server = "https://billingapi.apigw.gov-ntruss.com"

billing_api_server = "https://billingapi.apigw.ntruss.com"

getContractDemandCostList_api_url = "/billing/v1/cost/getContractDemandCostList"
getContractDemandCostList_api_url = (
    getContractDemandCostList_api_url
    + "?regionCode=KR&responseFormatType=json&startMonth={}&endMonth={}".format(
        yyyymm, yyyymm
    )
)

getDemandCostList_api_url = "/billing/v1/cost/getDemandCostList"
getDemandCostList_api_url = (
    getDemandCostList_api_url
    + "?regionCode=KR&responseFormatType=json&startMonth={}&endMonth={}".format(
        yyyymm, yyyymm
    )
)

getProductDemandCostList_api_url = "/billing/v1/cost/getProductDemandCostList"
getProductDemandCostList_api_url = (
    getProductDemandCostList_api_url
    + "?regionCode=KR&startMonth={}&endMonth={}&responseFormatType=json".format(
        yyyymm, yyyymm
    )
)

mail_api_server = "https://mail.apigw.ntruss.com"
mail_api_url = "/api/v1/mails"

body = {
    "senderAddress": "noreply@tcping.kr",
    "title": "[VIP2팀] 네이버클라우드 테스트 계정 사용내역 보고",
    "body": """
    <br>
    [민간]
    <br>
    VIP2팀의 {}월1일부터 {}월{}일까지의 총 이용금액과 내역은 아래와 같습니다.
    <br>
    <br>
    - 총 이용금액: 0원
    <br>
    <br>
    - 이용내역
    <br>
    <table border="2" class="dataframe">
    <thead>
        <tr style="text-align: center;">
        <th style="min-width: 250px;">서비스</th>     
        <th style="min-width: 50px;">사용금액(원)</th>
        <th style="min-width: 50px;">오래된 자원 생성일</th>
        </tr>
    </thead>
    </table>
    <br>
    [공공]
    <br>
    VIP2팀의 {}월1일부터 {}월{}일까지의 총 이용금액과 내역은 아래와 같습니다.
    <br>
    <br>
    - 총 이용금액: 0원
    <br>
    <br>
    - 이용내역
    <br>
    <table border="2" class="dataframe">
    <thead>
        <tr style="text-align: center;">
        <th style="min-width: 250px;">서비스</th>     
        <th style="min-width: 50px;">사용금액(원)</th>
        <th style="min-width: 50px;">오래된 자원 생성일</th>
        </tr>
    </thead>
    </table>
    <br>
<p>※ 서비스 비용이 0원일 경우 표기하지 않습니다.<br aria-hidden="true" />※ 생성일이 <span style="color: #ff0000;">오래된 자원은 불필요 자원일 가능성이 있으니 확인</span> 바랍니다.<br aria-hidden="true" />※ 총 이용금액이 전일 발송 금액보다 큰 차이가 날 경우 콘솔에서 상세 내역을 확인해 주세요.</p>
                &nbsp;&nbsp;&nbsp;<a href= "https://www.ncloud.com/nsa/didim365tstest?returnUrl=https://www.ncloud.com/mypage/status/usage">[SubAccount 로그인]</a>
    
    """.format(
        date.month, date.month, (date.day) - 1, date.month, date.month, (date.day) - 1
    ),
    "individual": True,
    "advertising": False,
    "recipients": [
        {"address": "ts@didim365.com", "type": "R"},
    ],
}
