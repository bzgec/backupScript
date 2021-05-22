#!/bin/sh

# test:
# - World_old.txt is deleted
# - World_new.txt is added
# - Hello.txt contect is updated
# test_multiPath:
# - multi disk/path backup works
# - World_old.txt is deleted
# - World_new.txt is added
# - Hello.txt contect is updated
# test_no-delete:
# - Hello_old.txt and World_old.txt are keept
# - Hello_new.txt and World_new.txt are created
# test_exclude:
# - no backup of exclude_folder
# - no backup of *.adoc files (nor in root folder nor in sub_folder)

OUTPUT_FILE_RESULT=./test/output.txt
OUTPUT_FILE_EXPECTED=./test/output_expected.txt

prepare_test() {
    rm -rf ./test/dest/*
    rm -rf ./test/src
    (
        cd ./test || exit 2
        tar -zxf src.tar.gz
    )
}

run_test() {
    # python backup.py -c testConfig.py
    python backup.py -a -n -c testConfig.py >> ./test/test.log

    mv ./test/src/test/World_old.txt ./test/src/test/World_new.txt
    echo Updated > ./test/src/test/Hello.txt

    mv ./test/src/test_multiPath/test/World_old.txt ./test/src/test_multiPath/test/World_new.txt
    echo Updated > ./test/src/test_multiPath/test/Hello.txt

    mv ./test/src/test_no-delete/Hello_old.txt ./test/src/test_no-delete/Hello_new.txt
    mv ./test/src/test_no-delete/World_old.txt ./test/src/test_no-delete/World_new.txt

    # python backup.py -c testConfig.py
    python backup.py -a -n -c testConfig.py >> ./test/test.log
}

gen_output_file() {
    SEPARATOR="################################################################################"

    {
        echo $SEPARATOR
        find ./test/dest/*

        echo $SEPARATOR
        echo "echo test/Hello.txt"
        cat ./test/dest/test/Hello.txt

        echo $SEPARATOR
        echo "echo test_multiPath/test/Hello.txt"
        cat ./test/dest/test_multiPath/test/Hello.txt
    } > $OUTPUT_FILE_RESULT

    # echo $SEPARATOR > $OUTPUT_FILE_RESULT
    # find ./test/dest/* >> $OUTPUT_FILE_RESULT

    # echo $SEPARATOR >> $OUTPUT_FILE_RESULT
    # echo "test/Hello.txt" >> $OUTPUT_FILE_RESULT
    # cat ./test/dest/test/Hello.txt >> $OUTPUT_FILE_RESULT

    # echo $SEPARATOR >> $OUTPUT_FILE_RESULT
    # echo "test_multiPath/test/Hello.txt" >> $OUTPUT_FILE_RESULT
    # cat ./test/dest/test_multiPath/test/Hello.txt >> $OUTPUT_FILE_RESULT
}

check_output_file() {
    if cmp -s $OUTPUT_FILE_EXPECTED $OUTPUT_FILE_RESULT; then
        echo "Test OK"
        exit 0
    else
        echo "TEST FAILED!!!"
        exit 1
    fi
    # cmp -s $OUTPUT_FILE_EXPECTED $OUTPUT_FILE_RESULT
    # if [ $? -ne 0 ]; then
    #     echo "TEST FAILED!!!"
    #     exit 1
    # else
    #     echo "Test OK"
    #     exit 0
    # fi
}

prepare_test
run_test
gen_output_file
check_output_file
