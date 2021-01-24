from pykrx.website.krx.krxio import KrxWebIo, KrxFileIo, SrtWebIo
import pandas as pd
from pandas import DataFrame

# ------------------------------------------------------------------------------------------
# Ticker

class 상장종목검색(KrxWebIo):
    @property
    def bld(self):
        return "dbms/comm/finder/finder_stkisu"

    def fetch(self, mktsel: str="ALL", searchText: str = "") -> DataFrame:
        """[12003] 개별종목 시세 추이에서 검색 버튼 눌러 활성화 되는 종목 검색창 스크래핑

        Args:
            mktsel     (str, optional): 조회 시장 (STK/KSQ/ALL)
            searchText (str, optional): 검색할 종목명 -  입력하지 않을 경우 전체

        Returns:
            DataFrame : 상장 종목 정보를 반환

                  full_code short_code    codeName marketCode marketName marketEngName ord1 ord2
            0  KR7060310000     060310          3S        KSQ     코스닥        KOSDAQ        16
            1  KR7095570008     095570  AJ네트웍스        STK   유가증권         KOSPI        16
            2  KR7006840003     006840    AK홀딩스        STK   유가증권         KOSPI        16
            3  KR7054620000     054620   APS홀딩스        KSQ     코스닥        KOSDAQ        16
            4  KR7265520007     265520    AP시스템        KSQ     코스닥        KOSDAQ        16
        """
        result = self.read(mktsel=mktsel, searchText=searchText, typeNo=0)
        return DataFrame(result['block1'])


class 상폐종목검색(KrxWebIo):
    @property
    def bld(self):

        return "dbms/comm/finder/finder_listdelisu"

    def fetch(self, mktsel:str = "ALL", searchText: str = "") -> DataFrame:
        """[20037] 상장폐지종목 현황
         - http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC02021301

        Args:
            mktsel     (str, optional): 조회 시장 (STK/KSQ/ALL) . Defaults to "ALL".
            searchText (str, optional): 검색할 종목명으로 입력하지 않을 경우 전체 조회

        Returns:
            DataFrame: 상장폐지 종목 정보를 반환

                         full_code short_code    codeName marketCode   marketName ord1 ord2
                0     KR7037730009     037730         3R        KSQ        코스닥        16
                1     KR7036360006     036360      3SOFT        KSQ        코스닥        16
                2     KYG887121070     900010 3노드디지탈       KSQ        코스닥        16
                3     KR7038120002     038120    AD모터스       KSQ        코스닥        16
        """
        result = self.read(mktsel=mktsel, searchText=searchText, typeNo=0)
        return DataFrame(result['block1'])

# ------------------------------------------------------------------------------------------
# Market

class 개별종목시세(KrxWebIo):
    @property
    def bld(self):
        return "dbms/MDC/STAT/standard/MDCSTAT01701"

    def fetch(self, strtDd: str, endDd: str, isuCd: str) -> DataFrame:
        """[12003] 개별종목 시세 추이 (수정종가 아님)

        Args:
            strtDd (str): 조회 시작 일자 (YYMMDD)
            endDd  (str): 조회 종료 일자 (YYMMDD)
            isuCd  (str): 조회 종목 ISIN

        Returns:
            DataFrame: 일자별 시세 조회 결과
                   TRD_DD TDD_CLSPRC FLUC_TP_CD CMPPREVDD_PRC FLUC_RT TDD_OPNPRC TDD_HGPRC TDD_LWPRC  ACC_TRDVOL         ACC_TRDVAL               MKTCAP      LIST_SHRS
            0  2021/01/15     88,000          2        -1,700   -1.90     89,800    91,800    88,000  33,431,809  2,975,231,937,664  525,340,864,400,000  5,969,782,550
            1  2021/01/14     89,700          3             0    0.00     88,700    90,000    88,700  26,393,970  2,356,661,622,700  535,489,494,735,000  5,969,782,550
            2  2021/01/13     89,700          2          -900   -0.99     89,800    91,200    89,100  36,068,848  3,244,066,562,850  535,489,494,735,000  5,969,782,550
            3  2021/01/12     90,600          2          -400   -0.44     90,300    91,400    87,800  48,682,416  4,362,546,108,950  540,862,299,030,000  5,969,782,550
            4  2021/01/11     91,000          1         2,200    2.48     90,000    96,800    89,500  90,306,177  8,379,237,727,064  543,250,212,050,000  5,969,782,550
        """
        result = self.read(isuCd=isuCd, strtDd=strtDd, endDd=endDd)
        return DataFrame(result['output'])


class 전종목시세(KrxWebIo):
    @property
    def bld(self):
        return "dbms/MDC/STAT/standard/MDCSTAT01501"

    def fetch(self, trdDd: str, mktId: str) -> DataFrame:
        """[12001] 전종목 시세

        Args:
            trdDd (str): 조회 일자 (YYMMDD)
            mktId (str): 조회 시장 (STK/KSQ/KNX/ALL)

        Returns:
            DataFrame: 전종목의 가격 정보

                 ISU_SRT_CD    ISU_ABBRV  MKT_NM     SECT_TP_NM TDD_CLSPRC FLUC_TP_CD CMPPREVDD_PRC FLUC_RT TDD_OPNPRC TDD_HGPRC TDD_LWPRC ACC_TRDVOL     ACC_TRDVAL           MKTCAP    LIST_SHRS MKT_ID
            0        060310           3S  KOSDAQ     중견기업부      2,365          2            -5   -0.21      2,370     2,395     2,355    152,157    361,210,535  105,886,118,195   44,772,143    KSQ
            1        095570   AJ네트웍스   KOSPI                     5,400          1            70    1.31      5,330     5,470     5,260     90,129    485,098,680  252,840,393,000   46,822,295    STK
            2        068400     AJ렌터카   KOSPI                    12,000          1           400    3.45     11,600    12,000    11,550    219,282  2,611,434,750  265,755,600,000   22,146,300    STK
            3        006840     AK홀딩스   KOSPI                    55,000          1           800    1.48     54,700    55,300    53,600     16,541    901,619,600  728,615,855,000   13,247,561    STK
            4        054620    APS홀딩스  KOSDAQ     우량기업부      4,475          1            10    0.22      4,440     4,520     4,440     31,950    142,780,675   91,264,138,975   20,394,221    KSQ
        """
        result = self.read(mktId=mktId, trdDd=trdDd)
        return DataFrame(result['OutBlock_1'])


class PER_PBR_배당수익률_전종목(KrxWebIo):
    @property
    def bld(self):
        return "dbms/MDC/STAT/standard/MDCSTAT03501"

    def fetch(self, trdDd: str, mktId: str) -> DataFrame:
        """[12021] PER/PBR/배당수익률

        Args:
            trdDd (str): 조회 일자 (YYMMDD)
            mktId (str): 조회 시장 (STK/KSQ/KNX/ALL)

        Returns:
            DataFrame:
                     ISU_SRT_CD   ISU_ABBRV                      ISU_ABBRV_STR TDD_CLSPRC FLUC_TP_CD CMPPREVDD_PRC FLUC_RT    EPS    PER     BPS   PBR  DPS DVD_YLD
                0        060310         3S            3S <em class ="up"></em>      2,195          1            20    0.92      -      -     745  2.95    0    0.00
                1        095570   AJ네트웍스  AJ네트웍스 <em class ="up"></em>      4,560          1            20    0.44    982   4.64   6,802  0.67  300    6.58
                2        006840    AK홀딩스     AK홀딩스 <em class ="up"></em>     27,550          1         2,150    8.46  2,168  12.71  62,448  0.44  750    2.72
                3        054620   APS홀딩스    APS홀딩스 <em class ="up"></em>      6,920          2          -250   -3.49      -      -  10,530  0.66    0    0.00
                4        265520    AP시스템     AP시스템 <em class ="up"></em>     25,600          1           600    2.40    671  38.15   7,468  3.43   50    0.20
        """
        result = self.read(mktId=mktId, trdDd=trdDd)
        return DataFrame(result['output'])


class PER_PBR_배당수익률_개별(KrxWebIo):
    @property
    def bld(self):
        return "dbms/MDC/STAT/standard/MDCSTAT03502"

    def fetch(self, strtDd: str, endDd: str, mktId: str, isuCd: str) -> DataFrame:
        """[12021] PER/PBR/배당수익률

        Args:
            strtDd (str): 조회 시작 일자 (YYMMDD)
            endDd  (str): 조회 종료 일자 (YYMMDD)
             mktId (str): 조회 시장 (STK/KSQ/KNX/ALL)
            isuCd  (str): 조회 종목 ISIN

        Returns:
            DataFrame:
                       TRD_DD TDD_CLSPRC FLUC_TP_CD CMPPREVDD_PRC FLUC_RT    EPS   PER     BPS   PBR  DPS DVD_YLD
                0  2019/03/29     44,650          2          -200   -0.45  5,997  7.45  28,126  1.59  850    1.90
                1  2019/03/28     44,850          2          -500   -1.10  5,997  7.48  28,126  1.59  850    1.90
                2  2019/03/27     45,350          1           100    0.22  5,997  7.56  28,126  1.61  850    1.87
                3  2019/03/26     45,250          2          -250   -0.55  5,997  7.55  28,126  1.61  850    1.88
                4  2019/03/25     45,500          2        -1,050   -2.26  5,997  7.59  28,126  1.62  850    1.87

        """
        result = self.read(mktId=mktId, strtDd=strtDd, endDd=endDd, isuCd=isuCd)
        return DataFrame(result['output'])


class 전종목등락률(KrxWebIo):
    @property
    def bld(self):
        return "dbms/MDC/STAT/standard/MDCSTAT01602"

    def fetch(self, strtDd: str, endDd: str, mktId: str, adj_stkprc: int) -> DataFrame:
        """[12002] 전종목 등락률

        Args:
            strtDd     (str): 조회 시작 일자 (YYMMDD)
            endDd      (str): 조회 종료 일자 (YYMMDD)
            mktId      (str): 조회 시장 (STK/KSQ/ALL)
            adj_stkprc (int): 수정 종가 여부 (2:수정종가/1:단순종가)

        Returns:
            DataFrame:
                  ISU_SRT_CD    ISU_ABBRV BAS_PRC TDD_CLSPRC CMPPREVDD_PRC FLUC_RT  ACC_TRDVOL       ACC_TRDVAL FLUC_TP
                0     060310           3S   2,420      3,290           870   35.95  40,746,975  132,272,050,410       1
                1     095570   AJ네트웍스   6,360      5,430          -930  -14.62   3,972,269   23,943,953,170       2
                2     068400     AJ렌터카  13,550     11,500        -2,050  -15.13  14,046,987  166,188,922,890       2
                3     006840     AK홀딩스  73,000     77,100         4,100    5.62   1,707,900  132,455,779,600       1
                4     054620    APS홀딩스   6,550      5,560          -990  -15.11   7,459,926   41,447,809,620       2
        """
        result = self.read(mktId=mktId, adj_stkprc=adj_stkprc, strtDd=strtDd,
                           endDd=endDd)
        return DataFrame(result['OutBlock_1'])


class 외국인보유량_전종목(KrxWebIo):
    @property
    def bld(self):
        return "dbms/MDC/STAT/standard/MDCSTAT03701"

    def fetch(self, trdDd: str, mktId: str, isuLmtRto: int) -> DataFrame:
        """[12023] 외국인보유량(개별종목) - 전종목

        Args:
            trdDd     (str): 조회 일자 (YYMMDD)
            mktId     (str): 조회 시장 (STK/KSQ/KNX/ALL)
            isuLmtRto (int): 외국인 보유제한 종목
            - 0 : check X
            - 1 : check O

        Returns:
            DataFrame:
                  ISU_SRT_CD   ISU_ABBRV TDD_CLSPRC FLUC_TP_CD CMPPREVDD_PRC FLUC_RT   LIST_SHRS FORN_HD_QTY FORN_SHR_RT FORN_ORD_LMT_QTY FORN_LMT_EXHST_RT
                0     060310          3S      2,185          2           -10   -0.46  44,802,511     739,059        1.65       44,802,511              1.65
                1     095570  AJ네트웍스      4,510          2           -50   -1.10  46,822,295   4,983,122       10.64       46,822,295             10.64
                2     006840    AK홀딩스     26,300          2        -1,250   -4.54  13,247,561   1,107,305        8.36       13,247,561              8.36
                3     054620   APS홀딩스      7,010          1            90    1.30  20,394,221     461,683        2.26       20,394,221              2.26
                4     265520    AP시스템     25,150          2          -450   -1.76  14,480,227   1,564,312       10.80       14,480,227             10.80
        """
        result = self.read(searchType=1, mktId=mktId, trdDd=trdDd, isuLmtRto=isuLmtRto)
        return DataFrame(result['output'])


class 외국인보유량_개별추이(KrxWebIo):
    @property
    def bld(self):
        return "dbms/MDC/STAT/standard/MDCSTAT03702"

    def fetch(self, strtDd: str, endDd: str, isuCd: str) -> DataFrame:
        """[12023] 외국인보유량(개별종목) - 개별추이

        Args:
            strtDd (str): 조회 시작 일자 (YYMMDD)
            endDd  (str): 조회 종료 일자 (YYMMDD)
            isuCd  (str): 조회 종목 ISIN

        Returns:
            DataFrame:
                       TRD_DD TDD_CLSPRC FLUC_TP_CD CMPPREVDD_PRC FLUC_RT      LIST_SHRS    FORN_HD_QTY FORN_SHR_RT FORN_ORD_LMT_QTY FORN_LMT_EXHST_RT
                0  2021/01/15     88,000          2        -1,700   -1.90  5,969,782,550  3,317,574,926       55.57    5,969,782,550             55.57
                1  2021/01/14     89,700          3             0    0.00  5,969,782,550  3,314,652,740       55.52    5,969,782,550             55.52
                2  2021/01/13     89,700          2          -900   -0.99  5,969,782,550  3,316,551,070       55.56    5,969,782,550             55.56
                3  2021/01/12     90,600          2          -400   -0.44  5,969,782,550  3,318,676,206       55.59    5,969,782,550             55.59
                4  2021/01/11     91,000          1         2,200    2.48  5,969,782,550  3,324,115,988       55.68    5,969,782,550             55.68
        """
        result = self.read(searchType=2, strtDd=strtDd, endDd=endDd, isuCd=isuCd)
        return DataFrame(result['output'])


class 투자자별_거래실적_전체시장_기간합계(KrxWebIo):
    @property
    def bld(self):
        return "dbms/MDC/STAT/standard/MDCSTAT02201"

    def fetch(self, strtDd: str, endDd: str, mktId: str, etf: str, etn: str, els: str) -> DataFrame:
        """[12009] 투자자별 거래실적

        Args:
            strtDd (str): 조회 시작 일자 (YYMMDD)
            endDd  (str): 조회 종료 일자 (YYMMDD)
            mktId  (str): 조회 시장 (STK/KSQ/ALL)
            etf    (str): ETF 포함 여부 (""/EF)
            etn    (str): ETN 포함 여부 (""/EN)
            els    (str): ELS 포함 여부 (""/ES)

        Returns:
            DataFrame:
                     INVST_TP_NM      ASK_TRDVOL      BID_TRDVOL NETBID_TRDVOL           ASK_TRDVAL           BID_TRDVAL       NETBID_TRDVAL
                0       금융투자     183,910,512     173,135,582   -10,774,930   11,088,878,744,833   10,518,908,333,291    -569,970,411,542
                1           보험      18,998,546      11,995,538    -7,003,008    1,011,736,647,106      661,574,577,285    -350,162,069,821
                2           투신      78,173,801      64,724,900   -13,448,901    2,313,376,665,370    1,943,337,885,168    -370,038,780,202
                3           사모      37,867,724      33,001,267    -4,866,457    1,142,499,274,494    1,000,228,858,448    -142,270,416,046
                4           은행       3,252,303         901,910    -2,350,393       69,744,809,430       43,689,969,205     -26,054,840,225
        """
        result = self.read(strtDd=strtDd, endDd=endDd, mktId=mktId, etf=etf, etn=etn, elw=els)
        return DataFrame(result['output']).drop('CONV_OBJ_TP_CD', axis=1)


class 투자자별_거래실적_전체시장_일별추이_일반(KrxWebIo):
    @property
    def bld(self):
        return "dbms/MDC/STAT/standard/MDCSTAT02202"

    def fetch(self, strtDd: str, endDd: str, mktId: str, etf: str, etn: str, els: str, trdVolVal: int, askBid: int) -> DataFrame:
        """[12009] 투자자별 거래실적 일별추이

        Args:
            strtDd     (str): 조회 시작 일자 (YYMMDD)
            endDd      (str): 조회 종료 일자 (YYMMDD)
            mktId      (str): 조회 시장 (STK/KSQ/ALL)
            etf        (str): ETF 포함 여부 (""/EF)
            etn        (str): ETN 포함 여부 (""/EN)
            els        (str): ELS 포함 여부 (""/ES)
            trdVolVal  (int): 1: 거래량 / 2: 거래대금
            askBid     (int): 1: 매도 / 2: 매수 / 3: 순매수

        Returns:
            DataFrame:

                >> 투자자별_거래실적_전체시장_일별추이_일반().fetch("20210115", "20210122", "STK", "", "", "", 1, 1)

                       TRD_DD     TRDVAL1     TRDVAL2        TRDVAL3      TRDVAL4     TRDVAL_TOT
                0  2021/01/22  67,656,491   6,020,990    927,119,399  110,426,104  1,111,222,984
                1  2021/01/21  69,180,642  13,051,423  1,168,810,381  109,023,034  1,360,065,480
                2  2021/01/20  70,184,991   5,947,195  1,010,578,768  105,984,335  1,192,695,289
                3  2021/01/19  56,242,065   6,902,124  1,183,520,475  106,647,770  1,353,312,434
                4  2021/01/18  70,527,745   7,512,434  1,270,483,687  123,524,707  1,472,048,573
        """
        result = self.read(strtDd=strtDd, endDd=endDd, mktId=mktId, etf=etf, etn=etn, elw=els, inqTpCd=2, trdVolVal=trdVolVal,
                           askBid=askBid)
        return DataFrame(result['output'])


class 투자자별_거래실적_전체시장_일별추이_상세(KrxWebIo):
    @property
    def bld(self):
        return "dbms/MDC/STAT/standard/MDCSTAT02203"

    def fetch(self, strtDd: str, endDd: str, mktId: str, etf: str, etn: str, els: str, trdVolVal: int, askBid: int) -> DataFrame:
        """[12009] 투자자별 거래실적 일별추이 (상세)

        Args:
            strtDd     (str): 조회 시작 일자 (YYMMDD)
            endDd      (str): 조회 종료 일자 (YYMMDD)
            mktId      (str): 조회 시장 (STK/KSQ/ALL)
            etf        (str): ETF 포함 여부 (""/EF)
            etn        (str): ETN 포함 여부 (""/EN)
            els        (str): ELS 포함 여부 (""/ES)
            trdVolVal  (int): 1: 거래량 / 2: 거래대금
            askBid     (int): 1: 매도 / 2: 매수 / 3: 순매수

        Returns:
            DataFrame:

                >> 투자자별_거래실적_전체시장_일별추이_상세().fetch("20210115", "20210122", "STK", "", "", "", 1, 1)

                       TRD_DD     TRDVAL1    TRDVAL2    TRDVAL3    TRDVAL4  TRDVAL5    TRDVAL6     TRDVAL7     TRDVAL8        TRDVAL9     TRDVAL10   TRDVAL11     TRDVAL_TOT
                0  2021/01/22  27,190,933  2,735,154  8,774,207  3,338,979  454,546    170,392  24,992,280   6,020,990    927,119,399  108,740,962  1,685,142  1,111,222,984
                1  2021/01/21  18,482,914  3,032,118  6,625,819  3,543,737  635,314  8,696,961  28,163,779  13,051,423  1,168,810,381  106,653,326  2,369,708  1,360,065,480
                2  2021/01/20  25,584,466  2,530,140  8,106,713  4,204,627  182,144    137,315  29,439,586   5,947,195  1,010,578,768  103,998,394  1,985,941  1,192,695,289
                3  2021/01/19  13,992,565  2,122,324  7,740,948  2,736,919  391,860    419,021  28,838,428   6,902,124  1,183,520,475  103,967,576  2,680,194  1,353,312,434
                4  2021/01/18  22,645,478  2,471,112  6,761,600  2,867,429  263,984    196,148  35,321,994   7,512,434  1,270,483,687  120,350,740  3,173,967  1,472,048,573
        """
        result = self.read(strtDd=strtDd, endDd=endDd, mktId=mktId, etf=etf, etn=etn, elw=els, trdVolVal=trdVolVal,
                           askBid=askBid, detailView=1)
        return DataFrame(result['output'])


class 투자자별_거래실적_개별종목_기간합계(KrxWebIo):
    @property
    def bld(self):
        return "dbms/MDC/STAT/standard/MDCSTAT02301"

    def fetch(self, strtDd: str, endDd: str, isuCd: str) -> DataFrame:
        """[12009] 투자자별 거래실적(개별종목)

        Args:
            strtDd    (str): 조회 시작 일자 (YYMMDD)
            endDd     (str): 조회 종료 일자 (YYMMDD)
            isuCd     (str): 조회 종목 ISIN

        Returns:
            DataFrame:
                     INVST_TP_NM   ASK_TRDVOL   BID_TRDVOL NETBID_TRDVOL          ASK_TRDVAL          BID_TRDVAL       NETBID_TRDVAL
                0       금융투자   31,324,444   28,513,421    -2,811,023   2,765,702,311,200   2,510,494,630,400    -255,207,680,800
                1           보험    1,790,469      561,307    -1,229,162     158,120,209,600      49,570,523,900    -108,549,685,700
                2           투신    3,966,211    1,486,178    -2,480,033     351,753,222,200     130,513,380,300    -221,239,841,900
                3           사모      756,726      541,912      -214,814      67,202,238,800      47,475,872,700     -19,726,366,100
                4           은행      105,323       70,598       -34,725       9,360,874,400       6,170,507,400      -3,190,367,000
        """
        result = self.read(strtDd=strtDd, endDd=endDd, isuCd=isuCd, inqTpCd=1, trdVolVal=1, askBid=1)
        return DataFrame(result['output']).drop('CONV_OBJ_TP_CD', axis=1)


class 투자자별_거래실적_개별종목_일별추이_일반(KrxWebIo):
    @property
    def bld(self):
        return "dbms/MDC/STAT/standard/MDCSTAT02302"

    def fetch(self, strtDd: str, endDd: str, isuCd: str, trdVolVal: int, askBid: int) -> DataFrame:
        """[12009] 투자자별 거래실적(개별종목)

        Args:
            strtDd     (str): 조회 시작 일자 (YYMMDD)
            endDd      (str): 조회 종료 일자 (YYMMDD)
            isuCd      (str): 조회 종목 ISIN
            trdVolVal  (int): 1: 거래량 / 2: 거래대금
            askBid     (int): 1: 매도 / 2: 매수 / 3: 순매수

        Returns:
            DataFrame:
                       TRD_DD     TRDVAL1  TRDVAL2     TRDVAL3    TRDVAL4  TRDVAL_TOT
                0  2021/01/20  13,121,791  114,341   7,346,474  4,628,521  25,211,127
                1  2021/01/19  13,912,581  323,382  20,956,376  4,702,705  39,895,044
                2  2021/01/18  15,709,256  258,096  21,942,253  5,318,346  43,227,951
                3  2021/01/15  16,944,750  216,653  10,371,182  5,899,224  33,431,809
                4  2021/01/14  15,722,824  232,674   6,483,589  3,954,883  26,393,970
        """
        result = self.read(strtDd=strtDd, endDd=endDd, isuCd=isuCd, inqTpCd=2, trdVolVal=trdVolVal, askBid=askBid)
        return DataFrame(result['output'])


class 투자자별_거래실적_개별종목_일별추이_상세(KrxWebIo):
    @property
    def bld(self):
        return "dbms/MDC/STAT/standard/MDCSTAT02303"

    def fetch(self, strtDd: str, endDd: str, isuCd: str, trdVolVal: int, askBid: int) -> DataFrame:
        """[12009] 투자자별 거래실적(개별종목)

        Args:
            strtDd     (str): 조회 시작 일자 (YYMMDD)
            endDd      (str): 조회 종료 일자 (YYMMDD)
            isuCd      (str): 조회 종목 ISIN
            trdVolVal  (int): 1: 거래량 / 2: 거래대금
            askBid     (int): 1: 매도 / 2: 매수 / 3: 순매수

        Returns:
            DataFrame:
                       TRD_DD    TRDVAL1  TRDVAL2    TRDVAL3  TRDVAL4 TRDVAL5 TRDVAL6     TRDVAL7  TRDVAL8     TRDVAL9   TRDVAL10 TRDVAL11  TRDVAL_TOT
                0  2021/01/20  5,328,172  259,546    313,812   58,992   3,449     256   7,157,564  114,341   7,346,474  4,615,231   13,290  25,211,127
                1  2021/01/19  2,835,217  119,057    312,695   42,163  10,100     180  10,593,169  323,382  20,956,376  4,644,854   57,851  39,895,044
                2  2021/01/18  4,175,051  286,158    349,739   98,050  11,261   4,486  10,784,511  258,096  21,942,253  5,262,225   56,121  43,227,951
                3  2021/01/15  7,080,570  272,542    838,871  112,920   1,691  21,958   8,616,198  216,653  10,371,182  5,878,858   20,366  33,431,809
                4  2021/01/14  6,926,895  366,023    707,874   67,391  25,022  10,072   7,619,547  232,674   6,483,589  3,937,223   17,660  26,393,970
                5  2021/01/13  4,978,539  487,143  1,443,220  377,210  53,800  74,669  10,728,979  122,212   9,029,353  8,746,689   27,034  36,068,848
        """
        result = self.read(strtDd=strtDd, endDd=endDd, isuCd=isuCd, inqTpCd=2, trdVolVal=trdVolVal, askBid=askBid, detailView=1)
        return DataFrame(result['output'])


class 투자자별_순매수상위종목(KrxWebIo):
    @property
    def bld(self):
        return "dbms/MDC/STAT/standard/MDCSTAT02401"

    def fetch(self, strtDd: str, endDd: str, mktId: str, invstTpCd: str) -> DataFrame:
        """[12010] 투자자별 순매수상위종목

        Args:
            strtDd    (str): 조회 시작 일자 (YYMMDD)
            endDd     (str): 조회 종료 일자 (YYMMDD)
            mktId     (str): 조회 시장 (STK/KSQ/KNX/ALL)
            invstTpCd (str): 투자자
             - 1000 - 금융투자
             - 2000 - 보험
             - 3000 - 투신
             - 3100 - 사모
             - 4000 - 은행
             - 5000 - 기타금융
             - 6000 - 연기금
             - 7050 - 기관합계
             - 7100 - 기타법인
             - 8000 - 개인
             - 9000 - 외국인
             - 9001 - 기타외국인
             - 9999 - 전체

        Returns:
            DataFrame:
                     ISU_SRT_CD        ISU_NM   ASK_TRDVOL   BID_TRDVOL NETBID_TRDVOL         ASK_TRDVAL         BID_TRDVAL     NETBID_TRDVAL
                0        006400       삼성SDI    1,298,644    1,636,929       338,285    899,322,500,000  1,125,880,139,000   226,557,639,000
                1        051910        LG화학    1,253,147    1,492,717       239,570  1,166,498,517,000  1,371,440,693,000   204,942,176,000
                2        096770  SK이노베이션    4,159,038    4,823,863       664,825  1,050,577,437,000  1,208,243,272,500   157,665,835,500
                3        003670  포스코케미칼    1,093,803    1,973,179       879,376    129,914,349,500    240,577,561,000   110,663,211,500
        """
        result = self.read(strtDd=strtDd, endDd=endDd, mktId=mktId, invstTpCd=invstTpCd)
        return DataFrame(result['output'])


# ------------------------------------------------------------------------------------------
# index

class 전체지수기본정보(KrxWebIo):
    @property
    def bld(self):
        return "dbms/MDC/STAT/standard/MDCSTAT00401"

    def fetch(self, idxIndMidclssCd: str) -> DataFrame:
        """[11004] 전체지수 기본정보

        Args:
            idxIndMidclssCd (str): 검색할 시장
             - 01 : KRX
             - 02 : KOSPI
             - 03 : KOSDAQ
             - 04 : 테마

        Returns:
            DataFrame: [description]
                    IDX_NM   IDX_ENG_NM BAS_TM_CONTN ANNC_TM_CONTN BAS_IDX_CONTN CALC_CYCLE_CONTN        CALC_TM_CONTN COMPST_ISU_CNT IND_TP_CD IDX_IND_CD
            0      KRX 300      KRX 300   2010.01.04    2018.02.05      1,000.00              1초  09:00:10 ~ 15:30:00            300         5        300
            1      KTOP 30      KTOP 30   1996.01.03    2015.07.13        888.85              2초  09:00:10 ~ 15:30:00             30         5        600
            2      KRX 100      KRX 100   2001.01.02    2005.06.01      1,000.00              1초  09:00:10 ~ 15:30:00            100         5        042
        """
        result = self.read(idxIndMidclssCd=idxIndMidclssCd)
        return DataFrame(result['output'])

class 주가지수검색(KrxWebIo):
    @property
    def bld(self):
        return "dbms/comm/finder/finder_equidx"

    def fetch(self, market: str) -> DataFrame:
        """[11004] 전체지수 기본정보

        Args:
            market (str): 검색 시장
             - 1 : 전체
             - 2 : KRX
             - 3 : KOSPI
             - 4 : KOSDAQ
             - 5 : 테마

        Returns:
            DataFrame:
                  full_code short_code     codeName marketCode marketName
                0         5        300      KRX 300        KRX        KRX
                1         5        600      KTOP 30        KRX        KRX
                2         5        042      KRX 100        KRX        KRX
                3         5        301  KRX Mid 200        KRX        KRX
                4         5        043   KRX 자동차        KRX        KRX

                marketCode : ['KRX' 'STK' 'KSQ' 'GBL']
                marketName : ['KRX' 'KOSPI' 'KOSDAQ' '테마']
        """
        result = self.read(mktsel=market)
        return DataFrame(result['block1'])


class 개별지수시세(KrxWebIo):
    @property
    def bld(self):
        return "dbms/MDC/STAT/standard/MDCSTAT00301"

    def fetch(self, ticker: str, group_id: str, fromdate: str, todate: str) -> DataFrame:
        """[11003] 개별지수 시세 추이

        Args:
            ticker   (str): index ticker
            group_id (str): index group id
            fromdate (str): 조회 시작 일자 (YYMMDD)
            todate   (str): 조회 종료 일자 (YYMMDD)

        Returns:
            DataFrame:
                       TRD_DD CLSPRC_IDX FLUC_TP_CD PRV_DD_CMPR UPDN_RATE OPNPRC_IDX HGPRC_IDX LWPRC_IDX  ACC_TRDVOL         ACC_TRDVAL               MKTCAP
                0  2021/01/15   2,298.05          2      -68.84     -2.91   2,369.94  2,400.69  2,292.92  22,540,416  1,967,907,809,615  137,712,088,395,380
                1  2021/01/14   2,366.89          2      -23.88     -1.00   2,390.59  2,393.24  2,330.76  23,685,783  2,058,155,913,335  142,206,993,223,695
                2  2021/01/13   2,390.77          1       25.68      1.09   2,367.94  2,455.05  2,300.10  33,690,790  3,177,416,322,985  144,549,058,033,310
                3  2021/01/12   2,365.09          2      -48.63     -2.01   2,403.51  2,428.76  2,295.91  41,777,076  3,933,263,957,150  143,250,319,286,660
                4  2021/01/11   2,413.72          1       33.32      1.40   2,403.37  2,613.83  2,352.21  50,975,686  6,602,833,901,895  146,811,113,380,140
        """
        result = self.read(indIdx2=ticker, indIdx=group_id, strtDd=fromdate, endDd=todate)
        return DataFrame(result['output'])

class 전체지수등락률(KrxWebIo):
    @property
    def bld(self):
        return "dbms/MDC/STAT/standard/MDCSTAT00201"

    def fetch(self, fromdate: str, todate: str, market: str) -> DataFrame:
        """[11002] 전체지수 등락률

        Args:
            fromdate (str): 조회 시작 일자 (YYMMDD)
            todate   (str): 조회 종료 일자 (YYMMDD)
            market   (str): 검색 시장
             - 01: KRX
             - 02: KOSPI
             - 03: KOSDAQ
             - 04: 테마

        Returns:
            DataFrame:
                        IDX_IND_NM OPN_DD_INDX END_DD_INDX FLUC_TP PRV_DD_CMPR FLUC_RT     ACC_TRDVOL           ACC_TRDVAL
                    0      KRX 300    1,845.82    1,920.52       1       74.70    4.05  3,293,520,227  201,056,395,899,602
                    1      KTOP 30   10,934.77   11,589.88       1      655.11    5.99    820,597,395  109,126,566,806,196
                    2      KRX 100    6,418.50    6,695.11       1      276.61    4.31  1,563,383,456  154,154,503,633,541
                    3  KRX Mid 200    1,751.19    1,722.32       2      -28.87   -1.65  2,807,696,801   27,059,313,040,039
                    4   KRX 자동차    2,046.67    2,298.05       1      251.38   12.28    288,959,592   29,886,192,965,797
        """
        result = self.read(idxIndMidclssCd=market, strtDd=fromdate, endDd=todate)
        return DataFrame(result['output'])


class 지수구성종목(KrxWebIo):
    @property
    def bld(self):
        return "dbms/MDC/STAT/standard/MDCSTAT00601"

    def fetch(self, date: str, ticker: str, group_id: str) -> DataFrame:
        """[11006] 지수구성종목

        Args:
            ticker   (str): index ticker
            group_id (str): index group id
            date     (str): 조회 일자 (YYMMDD)

        Returns:
            DataFrame:
                  ISU_SRT_CD     ISU_ABBRV TDD_CLSPRC FLUC_TP_CD STR_CMP_PRC FLUC_RT               MKTCAP MKTCAP_WT
                0     005930      삼성전자     46,850          1         600    1.30  279,684,312,467,500     19.54
                1     000660    SK하이닉스     78,100          2        -300   -0.38   56,856,984,706,500      3.97
                2     005380        현대차    126,500          2      -1,500   -1.17   27,029,025,655,500      1.89
                3     051910        LG화학    380,000          2      -8,500   -2.19   26,825,090,340,000      1.87
                4     068270      셀트리온    209,000          2      -1,500   -0.71   26,221,440,542,000      1.83
        """
        result = self.read(indIdx2=ticker, indIdx=group_id, trdDd=date)
        return DataFrame(result['output'])


################################################################################
# Shorting
class SRT02010100(KrxWebIo):
    @property
    def bld(self):
        return "SRT/02/02010100/srt02010100"

    @staticmethod
    def fetch(fromdate, todate, isin):
        """02010100 공매도 종합 현황
           http://short.krx.co.kr/contents/SRT/02/02010100/SRT02010100.jsp
        :param fromdate: 조회 시작 일자 (YYMMDD)
        :param todate: 조회 종료 일자 (YYMMDD)
        :param isin:
        :return: 공매도 종합 현황 DataFrame
        """
        result = SRT02010100().post(isu_cd=isin, strt_dd=fromdate, end_dd=todate)
        return DataFrame(result['block1'])


class SRT02020100(KrxFileIo):
    @property
    def bld(self):
        return "SRT/02/02020100/srt02020100"

    def fetch(self, fromedata, todate, market, isin):
        """02020100 공매도 거래 현황
           http://short.krx.co.kr/contents/SRT/02/02020100/SRT02020100.jsp
        :param fromdate: 조회 시작 일자 (YYMMDD)
        :param todate: 조회 종료 일자 (YYMMDD)
        :param market: 1 (코스피) / 3 (코스닥) / 4 (코넥스)
        :param isin: 종목의 ISIN
        :return:  종목별 공매도 거래 현황 DataFrame
        """

        result = self.post(mkt_tp_cd=market, isu_cd=isin, strt_dd=fromedata, end_dd=todate)
        return pd.read_excel(result)


class SRT02020300(KrxWebIo):
    @property
    def bld(self):
        return "SRT/02/02020300/srt02020300"

    @staticmethod
    def fetch(fromdate, todate, market=1, inquery=1):
        """02020300 공매도 거래 현황
           http://short.krx.co.kr/contents/SRT/02/02020300/SRT02020300.jsp
        :param fromdate: 조회 시작 일자 (YYMMDD)
        :param todate  : 조회 종료 일자 (YYMMDD)
        :param market  : 1 (코스피) / 2 (코스닥) / 6 (코넥스)
        :param inquery : 1 (거래대금) / 2 (거래량)
        :return: 투자자별 공매도 거래 현황 DataFrame
           str_const_val1 str_const_val2 str_const_val3 str_const_val4 str_const_val5      trd_dd
        0       1,161,522         37,396      6,821,963              0      8,020,881  2018/01/19
        1         970,406         41,242      8,018,997         13,141      9,043,786  2018/01/18
        2       1,190,006         28,327      8,274,090          6,465      9,498,888  2018/01/17
        """
        result = SRT02020300().post(mkt_tp_cd=market, inqCondTpCd=inquery, strt_dd=fromdate, end_dd=todate)
        return DataFrame(result['block1'])


class SRT02020400(KrxWebIo):
    @property
    def bld(self):
        return "SRT/02/02020400/srt02020400"

    @staticmethod
    def fetch(date, market=1):
        """02020400 공매도 거래 현황
           http://short.krx.co.kr/contents/SRT/02/02010100/SRT02010100.jsp
        :param date  : 조회 일자 (YYMMDD)
        :param market: 1 (코스피) / 2 (코스닥) / 6 (코넥스)
        :return: 공매도 거래비중 상위 50 종목 DataFrame
               acc_trdval      bas_dd cvsrtsell_trdval isu_abbrv        isu_cd  prc_yd rank srtsell_rto srtsell_trdval_avg tdd_srtsell_trdval_incdec_rt tdd_srtsell_wt valu_pd_avg_srtsell_wt
            0  35,660,149,500  2018/01/05   15,217,530,000     아모레퍼시픽  KR7090430000   0.334    1       2.877      7,945,445,875        1.915         42.674         14.834
            1     176,886,900  2018/01/05       69,700,600   영원무역홀딩스  KR7009970005   2.698    2       4.259         20,449,658        3.408         39.404          9.251
            2  27,690,715,500  2018/01/05    9,034,795,500             한샘  KR7009240003  -5.233    3       1.543      2,131,924,250        4.238         32.628         21.142
            3   2,444,863,350  2018/01/05      701,247,550             동서  KR7026960005  -0.530    4       2.820        255,763,771        2.742         28.682         10.172
        """
        result = SRT02020400().post(mkt_tp_cd=market, schdate=date)
        return DataFrame(result['block1'])


class SRT02030100(KrxFileIo):
    @property
    def bld(self):
        return "SRT/02/02030100/srt02030100"

    def fetch(self, fromdate, todate, market, isin):
        """02030100 공매도 잔고 현황
           http://short.krx.co.kr/contents/SRT/02/02010100/SRT02010100.jsp
        :param fromdate: 조회 시작 일자 (YYMMDD)
        :param todate  : 조회 종료 일자 (YYMMDD)
        :param market  : 1 (코스피) / 2 (코스닥) / 6 (코넥스)
        :param isin    : 조회 종목의 ISIN
        :return        : 종목별 공매도 잔고 현황 DataFrame
                  bal_amt  bal_qty bal_rto isu_abbrv        isu_cd    list_shrs              mktcap rn totCnt      trd_dd
            0  11,982,777,500  164,825    0.02    SK하이닉스  KR7000660001  728,002,365  52,925,771,935,500  1      7  2018/01/15
            1  12,427,999,200  167,043    0.02    SK하이닉스  KR7000660001  728,002,365  54,163,375,956,000  2      7  2018/01/12
            2  13,297,270,800  183,158    0.02    SK하이닉스  KR7000660001  728,002,365  52,852,971,699,000  3      7  2018/01/11
            3  14,594,580,000  200,200    0.03    SK하이닉스  KR7000660001  728,002,365  53,071,372,408,500  4      7  2018/01/10
        """

        result = self.post(mkt_tp_cd=market, strt_dd=fromdate, end_dd=todate, isu_cd=isin)
        return pd.read_excel(result)


class SRT02030400(KrxWebIo):
    @property
    def bld(self):
        return "SRT/02/02030400/srt02030400"

    @staticmethod
    def fetch(date, market=1):
        """02030400 공매도 잔고 현황
           http://short.krx.co.kr/contents/SRT/02/02020300/SRT02020300.jsp
        :param date  : 조회 일자 (YYMMDD)
        :param market: 1 (코스피) / 3 (코스닥) / 6 (코넥스)
        :return: 잔고 비중 상위 50 DataFrame
                       bal_amt    bal_qty bal_rto      isu_abbrv        isu_cd    list_shrs             mktcap rank rpt_duty_occr_dd    trd_dd
            0  190,835,680,350  5,323,171   10.12     한화테크윈  KR7012450003   52,600,000  1,885,710,000,000    1       2018/01/05  20180105
            1  161,456,413,600  2,570,962    9.45       현대위아  KR7011210002   27,195,083  1,707,851,212,400    2       2018/01/05  20180105
            2  147,469,396,800  9,131,232    8.58     두산중공업  KR7034020008  106,463,061  1,719,378,435,150    3       2018/01/05  20180105
            3  179,776,282,650  6,002,547    8.38         GS건설  KR7006360002   71,675,237  2,146,673,348,150    4       2018/01/05  20180105
        """
        result = SRT02030400().post(mkt_tp_cd=market, schdate=date)
        return DataFrame(result['block1'])


if __name__ == "__main__":
    pd.set_option('display.width', None)
    # stock
    # print(개별종목시세().fetch("20210110", "20210115", "KR7005930003"))
    # print(PER_PBR_배당수익률_전종목().fetch("20210115", "ALL"))
    # print(PER_PBR_배당수익률_개별().fetch('20190322', '20190329', 'ALL', 'KR7005930003'))
    # print(전종목등락률().fetch("20180501", "20180801", "ALL", 2))
    # print(외국인보유량_전종목().fetch("ALL", "20210115", 0))
    # print(외국인보유량_개별추이().fetch("20210108", "20210115", "KR7005930003"))

    # print(투자자별_거래실적_전체시장_기간합계().fetch("20210115", "20210122", "ALL", "", "", ""))
    # print(투자자별_거래실적_전체시장_기간합계().fetch("20210115", "20210122", "STK", "EF", "", ""))
    print(투자자별_거래실적_전체시장_일별추이_일반().fetch("20210115", "20210122", "STK", "", "", "", 1, 1))
    print(투자자별_거래실적_전체시장_일별추이_상세().fetch("20210115", "20210122", "STK", "", "", "", 1, 1))
    # ---
    # print(투자자별_거래실적_개별종목_기간합계().fetch("20210113", "20210120", "KR7005930003"))
    # print(투자자별_거래실적_개별종목_일별추이_일반().fetch("20210113", "20210120", "KR7005930003", 1, 1))
    # print(투자자별_거래실적_개별종목_일별추이_상세().fetch("20210113", "20210120", "KR7005930003", 1, 1))
    # print(투자자별_순매수상위종목().fetch("20201220", "20210120", "ALL", 1000))

    # index
    # df = 전체지수기본정보().fetch("04")
    # df = 전체지수등락률().fetch("20210107", "20210115", "01")
    # df = 주가지수검색().fetch("1")
    # df = 개별지수시세().fetch("043", "5", "20210107", "20210115")
    # df = 지수구성종목().fetch("20190412", "001", "1")

