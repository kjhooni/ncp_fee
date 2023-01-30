import call_api, var, recipients
import subprocess
import sys


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


def main(self):

    install("pandas")

    import pandas as pd
    from tkinter import CENTER

    #############################################   getDemandCostList
    for i in range(0, 3):
        res = call_api.func(
            i,
            var.apicall_method_get,
            var.billing_api_server,
            var.getDemandCostList_api_url,
            1,
        )
        ### 자원이 없으면 0원 메일 발송
        if res["getDemandCostListResponse"]["totalRows"] == 0:

            body = {
                "senderAddress": "noreply@tcping.kr",
                "title": "[운영{}팀] 네이버클라우드 테스트 계정 사용내역 보고".format(i + 1),
                "body": """
                <br>
                운영{}팀의 {}월1일부터 {}월{}일까지의 총 이용금액과 내역은 아래와 같습니다.
                <br>
                <br>
                - 총 이용금액: {}원
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
                <br>
    <p>※ 서비스 비용이 0원일 경우 표기하지 않습니다.<br aria-hidden="true" />※ 생성일이 <span style="color: #ff0000;">오래된 자원은 불필요 자원일 가능성이 있으니 확인</span> 바랍니다.<br aria-hidden="true" />※ 총 이용금액이 전일 발송 금액보다 큰 차이가 날 경우 콘솔에서 상세 내역을 확인해 주세요.</p>
                &nbsp;&nbsp;&nbsp;<a href= "https://www.ncloud.com/nsa/didim365se{}test?returnUrl=https://www.ncloud.com/mypage/status/usage">[SubAccount 로그인]</a>
                """.format(
                    i + 1,
                    var.date.month,
                    var.date.month,
                    (var.date.day) - 1,
                    totalUseAmount,
                    i + 1,
                ),
                "individual": True,
                "advertising": False,
                "recipients": [
                    {"address": recipients.list[i + 1], "type": "R"},
                ],
            }
            call_api.func(
                i, var.apicall_method_post, var.mail_api_server, var.mail_api_url, body
            )
            return {"payload": "true"}
        ###자원이 있으면
        else:

            totalUseAmount = res["getDemandCostListResponse"]["demandCostList"][0][
                var.uA
            ]
            totalUseAmount = format(totalUseAmount, ",d")

            ###API 호출

            res = call_api.func(
                i,
                var.apicall_method_get,
                var.billing_api_server,
                var.getProductDemandCostList_api_url,
                1,
            )

            totalRows = res[var.getproductde]["totalRows"]

            codeName = []
            useAmount = []

            for j in range(0, totalRows):
                if res[var.getproductde][var.productde][j][var.uA] == 0:
                    continue
                else:
                    codeName.append(
                        res[var.getproductde][var.productde][j]["productDemandType"][
                            "codeName"
                        ]
                    )
                    useAmount.append(res[var.getproductde][var.productde][j][var.uA])

            a = []
            ##2차원 빈 배열 생성

            for j in range(0, len(codeName)):
                line = []
                for k in range(3):  ##3개의 열
                    line.append(0)
                a.append(line)

            for j in range(0, len(codeName)):
                a[j][0] = codeName[j]
                a[j][1] = format(useAmount[j], ",d")
                a[j][2] = "자원 없음"

            ###API호출(자원 생성일 출력을 위한)
            res2 = call_api.func(
                i,
                var.apicall_method_get,
                var.billing_api_server,
                var.getContractDemandCostList_api_url,
                1,
            )

            total = len(
                res2["getContractDemandCostListResponse"]["contractDemandCostList"]
            )

            serviceCode = []
            contractStartDate = []
            contractEndDate = []

            for j in range(0, total):
                ##비용 발생한 자원의 경우
                if (
                    res2["getContractDemandCostListResponse"]["contractDemandCostList"][
                        j
                    ]["useAmount"]
                    > 0
                ):
                    serviceCode.append(
                        res2["getContractDemandCostListResponse"][
                            "contractDemandCostList"
                        ][j]["demandType"]["codeName"]
                    )
                    try:
                        contractStartDate.append(
                            res2["getContractDemandCostListResponse"][
                                "contractDemandCostList"
                            ][j]["contract"]["contractStartDate"]
                        )
                    except KeyError as k:
                        contractStartDate.append(var.today_date)
                    try:
                        contractEndDate.append(
                            res2["getContractDemandCostListResponse"][
                                "contractDemandCostList"
                            ][j]["contract"]["contractEndDate"]
                        )
                    except KeyError as k:
                        contractEndDate.append(var.today_date)

            ###yyyy-mm-dd 형태로 변환
            contractStartDate1 = []
            for j in contractStartDate:
                contractStartDate1.append(j[0:10])

            ###str 형태를 datetime 형태로 형변환
            contractStartDate2 = []
            for j in contractStartDate1:
                contractStartDate2.append(var.datetime.strptime(j, "%Y-%m-%d"))

            contractEndDate1 = []
            for j in contractEndDate:
                contractEndDate1.append(j[0:10])

            contractEndDate2 = []
            for j in contractEndDate1:
                contractEndDate2.append(var.datetime.strptime(j, "%Y-%m-%d"))

            ###빈 배열 생성
            arr = []
            for j in range(0, len(serviceCode)):
                line = []
                for k in range(3):
                    line.append(0)
                arr.append(line)

            ###빈 배열에 값 추가
            ###arr=[서비스명,계약시작일,계약종료일]
            for j in range(0, len(serviceCode)):
                arr[j][0] = serviceCode[j]
                arr[j][1] = contractStartDate2[j]
                arr[j][2] = contractEndDate2[j]

            c = []

            ###계약 종료 년도가 2999년 => 현재 이용중인 계약
            ###현재 이용중인 계약이 아닐 경우 arr에서 삭제
            for j in range(0, len(arr)):
                if arr[j][2].year != 2999:
                    c.append(j)

            for j in sorted(c, reverse=True):
                del arr[j]

            c = []

            ###서비스명이 같은 계약 중 서비스 계약일을 비교하여
            ###가장 오래전 생성된 자원만 남김(나중에 생성한 자원은 배열에서 삭제)
            for j in range(0, len(arr)):
                if j == len(arr) - 1:
                    break
                elif arr[j][0] == arr[j + 1][0]:
                    if arr[j][1] <= arr[j + 1][1]:  ###날짜의경우 최근일수록 더 큰 값임
                        c.append(j + 1)

            for j in sorted(c, reverse=True):
                del arr[j]

            ###기존 a배열과 arr배열의 서비스 명을 맵핑하여
            ###일치 할 경우 a배열의 3열에 계약 시작일 추가
            for j in range(0, len(arr)):
                for k in range(0, len(a)):
                    if arr[j][0] == a[k][0]:
                        a[k][2] = arr[j][1].strftime("%Y년%m월%d일")

            df = pd.DataFrame(a, columns=["서비스", "사용금액(원)", "오래된 자원 생성일"])
            to_html = df.to_html(
                index=False, col_space=[250, 50, 50], justify=CENTER, border=2
            )

            ###mailSend

            body = {
                "senderAddress": "noreply@tcping.kr",
                "title": "[운영{}팀] 네이버클라우드 테스트 계정 사용내역 보고".format(i + 1),
                "body": """
                <br>
                운영{}팀의 {}월1일부터 {}월{}일까지의 총 이용금액과 내역은 아래와 같습니다.
                <br>
                <br>
                - 총 이용금액: {}원
                <br>
                <br>
                - 이용내역
                <br>
                {}
                <br>
    <p>※ 서비스 비용이 0원일 경우 표기하지 않습니다.<br aria-hidden="true" />※ 생성일이 <span style="color: #ff0000;">오래된 자원은 불필요 자원일 가능성이 있으니 확인</span> 바랍니다.<br aria-hidden="true" />※ 총 이용금액이 전일 발송 금액보다 큰 차이가 날 경우 콘솔에서 상세 내역을 확인해 주세요.</p>
                &nbsp;&nbsp;&nbsp;<a href= "https://www.ncloud.com/nsa/didim365se{}test?returnUrl=https://www.ncloud.com/mypage/status/usage">[SubAccount 로그인]</a>
                """.format(
                    i + 1,
                    var.date.month,
                    var.date.month,
                    (var.date.day) - 1,
                    totalUseAmount,
                    to_html,
                    i + 1,
                ),
                "individual": True,
                "advertising": False,
                "recipients": [
                    {"address": recipients.list[i + 1], "type": "R"},
                ],
            }

            ###API호출(메일발송)
            call_api.func(
                i, var.apicall_method_post, var.mail_api_server, var.mail_api_url, body
            )

    return {"payload": "true"}
