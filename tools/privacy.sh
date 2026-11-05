#!/usr/bin/env bash
# La repo è pubblica: fallisce se nei file o nella cronologia c'è qualcosa da non pubblicare.
# Uso (dalla root della repo): bash tools/privacy.sh
fail=0

# email di autori e committer del branch corrente: solo noreply
emails=$(git log HEAD --format='%ae%n%ce' | sort -u | grep -v -E '@users\.noreply\.github\.com$|^noreply@(github|anthropic)\.com$')
[ -n "$emails" ] && { echo "Email non noreply nella cronologia:"; echo "$emails"; fail=1; }

# testi: percorsi personali, email personali, ID Steam, token
pattern='C:\\Users\\[A-Za-z0-9._-]+|/Users/[A-Za-z0-9._-]+|/home/[a-z]+/|765611[0-9]{11}|userdata[\\/][0-9]+|[A-Za-z0-9._%+-]+@(gmail|hotmail|yahoo|outlook|icloud|libero|live)\.[a-z]+|ghp_[A-Za-z0-9]+|github_pat_|sk-[A-Za-z0-9]{20,}'
git grep -I -n -E "$pattern" -- . ':!tools/privacy.sh' && { echo "Testi privati nei file (sopra)"; fail=1; }

# file: trascrizioni, grafica e testi del gioco, cache, log
files=$(git ls-files | grep -E 'trascrizioni/[^/]+\.txt$|Repentance\)\.png$|__pycache__|\.pyc$|^extracted/|^resources-dlc3/|\.log$|(^|/)log[^/]*\.txt$|\.env$|\.bundle$' | grep -v '^docs/trascrizioni/tormentoni\.txt$')
[ -n "$files" ] && { echo "File da non pubblicare:"; echo "$files"; fail=1; }

[ $fail = 0 ] && echo "PRIVACY OK"
exit $fail
