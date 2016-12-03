# -*- coding: utf-8 -*-

import sys
import Params
import dataGenerate
import data_preprocess


def main():
    download, writeln = False, False

    if len(sys.argv) == 3 and sys.argv[1] == 'T':
        try:
            lag_int = int(sys.argv[2])
        except(TypeError, ValueError):
            print("lag_int should be integer!")
            return
        if lag_int < 1:
            print("lag_int should be over zero!")
        rs = dataGenerate.DataGenerate(lag_int=lag_int, download=download, writeln=writeln)
    elif len(sys.argv) == 1:
        lag_int = 1
        rs = dataGenerate.DataGenerate(lag_int=lag_int, download=download, writeln=writeln)
    else:
        return
    print('Finish Loading!')

    result = data_preprocess.DataPreProcess(rs.ad_text, rs.user_ad)

    result.dot_seg()
    result.tag_extract()
    result.ad_tag()
    result.user_tag()
    print('Finish Segmenting!')

    file_path = dataGenerate.get_path()

    with open(file_path + Params.TAG, 'w') as f:
        for tag, weight in result.tag_weight.items():
            f.write(str(tag) + ':' + str(weight) + '\n')
    with open(file_path + Params.ADTAG, 'w') as f:
        for ad, tags in result.ad_tags.items():
            f.write(str(ad) + ':' + ' ')
            for tag in tags:
                f.write(str(tag[0]) + ' ')
            f.write('\n')
    with open(file_path + Params.USERTAG, 'w') as f:
        for user, tags in result.user_tags.items():
            f.write(str(user) + ':' + ' ')
            for tag in tags:
                f.write(str(tag[0]) + ' ')
            f.write('\n')
    print('Finish Writing!')
    return
if __name__ == '__main__':
    main()
