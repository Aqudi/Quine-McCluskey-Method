class McCluskeyCalculator:
    def __init__(self, v, m, m_list):
        self.num_v = v
        self.num_m = m
        self.minterms = m_list
        self.minterms = list(map(self.makeBin, self.minterms))

        # EPI를 걸러내기 위한 rank 사전
        self.rank = dict()
        for min in self.minterms:
            self.rank[min] = 0

        self.pi = []
        self.combinedHistory = dict()

    def makeBin(self, num):
        # bin함수 적용시 ob~~~나오므로 ob를 제거해줌
        # zfill()의 경우 앞의 0을 제거한 상태로 변환하니 편하게 계산하기 위해 맞춰줌
        return bin(num)[2:].zfill(self.num_v)

    def sortBy1(self, l):
        l = set(l)  # 중복된 것을 제거
        l = sorted(list(l), key=lambda x: x.count('1'))
        sorted_l = []
        temp = []
        before = l[0].count('1')
        for bin_num in l:
            current = bin_num.count('1')
            if before != current:
                sorted_l.append((before, temp))  # 1의 개수, 개수에 따른 리스트
                temp = [bin_num]  # temp를 다시 사용하기 위해 빈리스트 할당
            else:
                temp.append(bin_num)
            before = current
        sorted_l.append((before, temp))
        return sorted_l

    def check_possible(self, ex1, ex2):
        diff = 0
        idx = -1
        for i in range(self.num_v):
            # print("ex1: {}, ex2: {}, compare: {}".format(ex1[i], ex2[i], ex1[i] != ex2[i]))
            if ex1[i] != ex2[i]:
                diff += 1  # 같은 위치의 값이 다를 경우를 count
                idx = i  # 어디가 다른지 위치를 저장
        return (diff, idx)

    def processOverlapPart(self, l1, l2, result, combined):
        for first in l1:  # ex) 000(first)과 001, 010(second)을 차례대로 비교
            for second in l2:
                diff, idx = self.check_possible(first, second)
                # print("diff: {}, idx: {}, ".format(diff, idx), end="")
                # print("first : {}, second : {}".format(first, second))
                if diff != 1:  # 차이가 1이상이면 계산불가 다음 case로 넘어감
                    continue
                else:
                    temp = list(first)
                    temp[idx] = '2'
                    temp = "".join(temp)
                    result.append(temp)

                    combined.add(first)
                    combined.add(second)

                    history = []
                    if first in self.combinedHistory:
                        history.extend(self.combinedHistory[first])
                    else:
                        history.append(first)
                    if second in self.combinedHistory:
                        history.extend(self.combinedHistory[second])
                    else:
                        history.append(second)
                    self.combinedHistory[temp] = history
                # print("result : {}\n".format(result))

    def calculate(self):
        if not self.minterms:
            return -1
        sorted_by_1 = self.sortBy1(self.minterms)
        print(sorted_by_1)
        result = []  # 계산결과값을 저장할 리스트
        combined = set()  # 더 이상 결합할 수 없는 PI들을 저장할 리스트
        for i in range(0, len(sorted_by_1) - 1):  # 두 계층씩 짝을 묶어서 계산
            f_num1, f_list = sorted_by_1[i]  # 앞줄 ex) 1이 0개인 minterm들
            s_num1, s_list = sorted_by_1[i + 1]  # 뒷줄 ex) 1이 1개인 minterm들

            if s_num1 - f_num1 != 1:  # 조건 : 해밍거리가 1이어야지 계산가능함
                continue

            # 겹치는 부분들을 '-' 즉 2로 변경한 result리스트를 받음
            self.processOverlapPart(f_list, s_list, result, combined)

        # 더 이상 결합할 수 없는 요소 즉 PI들을 판별해서 저장한다.
        for check_combined in self.minterms:
            if check_combined not in combined:
                self.pi.append(check_combined)

        self.pi = sorted(list(set(self.pi)))
        print("PI : ", self.pi, "\n")
        self.minterms = result

    def distinguishEPIandNEPI(self):
        EPI = set({})
        NEPI = set(self.pi)
        
        for pi in self.pi:
            try:
                for value in self.combinedHistory[pi]:
                    self.rank[value] += 1
            except:
                print("except")
                for value in self.pi:
                    EPI.add(value)
        
        for key, value in self.rank.items():
            if value == 1:  # 한 번만 사용된 minterm을 가지고 있는 PI를 탐색
                for pi in self.pi:
                    if key in self.combinedHistory[pi]:
                        EPI.add(pi)
            # NEPI = set({})
        NEPI = NEPI - EPI
        EPI = map(self.twoToDash, sorted(list(EPI)))
        NEPI = map(self.twoToDash, sorted(list(NEPI)))
        return (list(EPI), list(NEPI))

    def twoToDash(self, value):
        return value.replace('2', '-')

def solution(i):
    num_v = i[0]  # 변수가 몇개인지
    num_m = i[1]  # 민텀이 몇개인지
    minterms = i[2:]  # 실제 민텀의 리스트
    mc = McCluskeyCalculator(num_v, num_m, minterms)

    isComplited = 0
    while not isComplited:
        isComplited = mc.calculate()

    e, n = mc.distinguishEPIandNEPI()
    EPI = ["EPI"] + e
    NEPI = ["NEPI"] + n
    answer = EPI + NEPI
    return answer
