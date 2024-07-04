import subprocess
import time

leela_path = r"..\lc0\lc0.exe"

leela = subprocess.Popen(leela_path,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         encoding='utf8',
                         bufsize=1)


def get_leela_move(think_time=.75, fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
    leela.stdin.write(f'position fen {fen} \n')
    leela.stdin.write(f'go \n')
    time.sleep(think_time)
    leela.stdin.write('stop \n')
    out, err = leela.communicate()
    return out.split("\n")[-2].split(" ")[1]


print(get_leela_move())

leela.terminate()
