def cafe_file():
    file_name = 'test.csv'  # index.__str__() + '_' + gu_name + '.'+'csv'
    file = open(file_name, 'w', encoding='utf-8')
    file.write("카페명" + "|" + "주소" + "|" + "영업시간" + "|" + "전화번호" + "|" + "대표사진주소" + "\n")
    return file