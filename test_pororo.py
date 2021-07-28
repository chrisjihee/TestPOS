from pororo import Pororo

pos = Pororo(task="pos", lang="ko")


def analyze_sent(sent: str):
    pairs = pos(sent)
    spaced = [[]]
    for lemma, tag in pairs:
        if tag == 'SPACE':
            spaced.append([])
        else:
            spaced[-1].append(f"{lemma}/{tag}")
    tagged = ' '.join(['+'.join(word) for word in spaced])
    return tagged


if __name__ == '__main__':
    원문 = "안녕하세요. 제 이름은 카터입니다."
    태깅 = analyze_sent(원문)
    print(원문)
    print(태깅)
