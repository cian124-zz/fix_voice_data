import os
import shutil

interesting_cols = [0]


def main():
    # Comment out line 103 and 104, run script
    # Uncomment lines 103 and 104, run script again
    # Comment out lines 103 and 104, run a final time
    correct_enroll_files()
    remove_files()


def correct_enroll_files():
    # Check for 3 files from 1 session in Enroll folder
    # If there are 3 files from 1 session, move extras to the Verify folder
    # Else, check for 3 files from 1 session in Verify folder
    # If there are 3 files from 1 session, copy them to the Enroll folder. Overwrite duplicates and then move extras to
    # the Verify folder
    # Else, remove both Enroll and Verify folder
    # Repeat for every folder in each Test data set

    enrolldir = "/Users/cmccormack/Daon/VoiceModelGeneration/RBS_English/TD_16k/Test1/roc_audio/enroll"
    verifydir = "/Users/cmccormack/Daon/VoiceModelGeneration/RBS_English/TD_16k/Test1/roc_audio/verify"
    global dir_done
    dir_done = True
    session_num = 3  # 3 for daon collect

    for subdir, dirs, files in os.walk(enrolldir):
        if dir_done:
            dir_done = False
            good_file_count = 0
            previous_file = ""
            for file in sorted(os.listdir(subdir)):
                if file.endswith('.wav'):
                    file_parts = file.split('_')
                    session_num = count_file_parts(file_parts)
                    if file_parts[session_num] == previous_file:
                        good_file_count += 1
                        previous_file = file_parts[session_num]
                    else:
                        previous_file = file_parts[session_num]
                        good_file_count = 1

                    if good_file_count == 3:
                        break

            if good_file_count == 3:
                for file in os.listdir(subdir):
                    if file.endswith(".wav"):
                        # print(file)
                        file_parts = file.split('_')
                        session_num = count_file_parts(file_parts)
                        if file_parts[session_num] != previous_file:
                            subject_id = subdir.split('/')[10]
                            # print(os.path.join(enrolldir, subdir, file))
                            # print(os.path.join(verifydir, subject_id, "V", file))
                            #
                            shutil.move(os.path.join(enrolldir, subdir, file),
                                        os.path.join(verifydir, subject_id, "V", file))
                dir_done = True
            else:
                good_file_count = 1
                if subdir.endswith("/E"):
                    subject_id = subdir.split('/')[10]
                    for file in sorted(os.listdir(os.path.join(verifydir, subject_id, "V"))):
                        # print(file)
                        if file.endswith(".wav"):
                            file_parts = file.split('_')
                            session_num = count_file_parts(file_parts)
                            if file_parts[session_num] == previous_file:
                                good_file_count += 1
                                previous_file = file_parts[session_num]
                            else:
                                previous_file = file_parts[session_num]
                                good_file_count = 1

                            if good_file_count == 3:
                                break
                    if good_file_count == 3:
                        for file in os.listdir(os.path.join(verifydir, subject_id, "V")):
                            if file.endswith(".wav"):
                                # print(file)
                                file_parts = file.split('_')
                                session_num = count_file_parts(file_parts)
                                if file_parts[session_num] == previous_file:
                                    subject_id = subdir.split('/')[10]
                                    # print(file)
                                    # print(os.path.join(enrolldir, subdir, file))
                                    # print(os.path.join(verifydir, subject_id, "V", file))
                                    shutil.move(os.path.join(verifydir, subject_id, "V", file),
                                                os.path.join(enrolldir, subdir, file))
                        for file in os.listdir(subdir):
                            if file.endswith(".wav"):
                                # print(file)
                                file_parts = file.split('_')
                                if file_parts[session_num] != previous_file:
                                    subject_id = subdir.split('/')[10]
                                    # print(os.path.join(enrolldir, subdir, file))
                                    # print(os.path.join(verifydir, subject_id, "V", file))
                                # comment out below two lines for first run, then uncomment and run again
                                # shutil.move(os.path.join(enrolldir, subdir, file),
                                #            os.path.join(verifydir, subject_id, "V", file))
                        dir_done = True

                    else:
                        if not subdir.endswith("/E"):
                            subject_id = subdir.split('/')[10]
                            shutil.move(subdir, os.path.join(enrolldir, "temp", "E"))
                            shutil.move(os.path.join(verifydir, subject_id), os.path.join(enrolldir, "temp", "V"))
                        # print(subdir)
                        dir_done = True

                dir_done = True


def remove_files():
    enrolldir = "/Users/cmccormack/Daon/VoiceModelGeneration/RBS_English/TD_16k/Test1/roc_audio/enroll"
    verifydir = "/Users/cmccormack/Daon/VoiceModelGeneration/RBS_English/TD_16k/Test1/roc_audio/verify"
    i = 0

    for subdir, dirs, files in os.walk(enrolldir):
        i = 0
        for file in sorted(os.listdir(subdir)):
            if file.endswith(".wav"):
                if i > 2:
                    os.remove(os.path.join(enrolldir, subdir, file))
                i += 1

    for subdir, dirs, files in os.walk(enrolldir):
        for file in sorted(os.listdir(subdir)):
            if file.endswith(".wav"):
                for v_subdir, v_dirs, v_files in os.walk(verifydir):
                    for v_file in os.listdir(subdir):
                        if v_file == file:
                            print(v_file + "  " + file)
                            # print(os.path.join(verifydir, v_file))
                            if os.path.exists(os.path.join(verifydir, v_subdir, v_file)):
                                os.remove(os.path.join(verifydir, v_subdir, v_file))


def count_file_parts(file_parts):
    if len(file_parts) == 6:
        return 3
    elif len(file_parts) == 4:
        return 2


if __name__ == '__main__':
    main()
