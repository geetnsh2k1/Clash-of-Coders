import sys
def particular_score(particular):
    if len(particular) == 1:
        return 100
    else:
        common = None
        flg = True
        max_count = 0   
        max_common = None
        for i in range(len(particular)-1):
            if flg:
                if len(particular[i]) > len(particular[i+1]):
                    for j in range(len(particular[i+1])-3):
                        sub_str = particular[i+1][j:j+4]
                        
                        count = 0
                        if sub_str in particular[i]:
                            for k in particular:
                                if sub_str in k:
                                    count += 1
                        if count == len(particular):
                            common = sub_str
                            flg = False
                            break
                        else: 
                            if count > max_count :
                                max_count = count
                                max_common = sub_str
                else:
                    for j in range(len(particular[i])-3):
                        sub_str = particular[i][j:j+4]
                        
                        count = 0
                        if sub_str in particular[i+1]:
                            for k in particular:
                                if sub_str in k:
                                    count += 1
                        if count == len(particular):
                            common = sub_str
                            flg = False
                            break
                        else: 
                            if count > max_count : 
                                max_count = count
                                max_common = sub_str
        
        score = 0
        x = 100
        if common != None:
            for word in particular:
                index = word.index(common)
                factor = index/(len(word)-3)
                if factor >= 0 and factor <= 0.33:
                    score += 25*x
                elif factor > 0.33 and factor <= 0.67:
                    score += 10*x
                else:
                    score += 5*x
        else:
            # max_count, #max_common
            if max_common != None:
                for word in particular:
                    if max_common in word:
                        index = word.index(max_common)
                        factor = index/(len(word)-3)
                        if factor >= 0 and factor <= 0.33:
                            score += 25*x
                        elif factor > 0.33 and factor <= 0.67:
                            score += 10*x
                        else:
                            score += 5*x
                        max_count -= 1
                    if max_count == 0:
                        break
    return score

def tuneup(s):
    if s == "'" or s.isalnum():
        return True
    else:
        return False

def calculate_score(data, actual):
    score = 0
    words = []
    actual = ["".join(filter(tuneup, word.lower())) for word in actual]

    for line in data:
        line = line.split(":")
        if line == ['']:
            continue
        line_words = line[0].split(",")
        
        particular = []
        
        for word in line_words:
            if " " in word:
                word = word.replace(" ", "")
            if word.lower() not in words:
                if word.lower() in actual:
                    particular.append(word.lower())
                    words.append(word.lower())
        score += particular_score(particular)
    
    return score

if __name__ == '__main__':
    data = None
    try:
        # with open("./mehul/output_p.txt", "r") as file:
            # data = file.read()
        # words = None
        # with open("./datasets/l.txt", "r") as file:
        #     words = set(file.read().split())
        
        res = sys.stdin.read().split('!-Next Dataset-!')
        
        print(len(res))
        ans = []
        total = 0
        for ip in res:
            if ip == '':
                break
            ip = ip.split('!-dataset-!')
            data = ip[0].split("\n")
            words = ip[1].split()
            
            words = set(words)
            
            temp = (calculate_score(data, words))
            print(temp)
            total += temp
            ans.append(temp)
        print(ans, total)
    except Exception as e:
        print(e)
        print("No File!")