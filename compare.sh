#!/bin/bash
shopt -s expand_aliases

alias testcase_generator=""
alias your_solution=""
alias naive_solution=""

declare -i max_number_of_attempts=
declare -i max_number_of_WA_or_RE=

### ==================================== ###

# Make a directory called compare
if [ ! -d ./compare ]; then
  mkdir compare
fi

declare -i WA_count=0
declare -i RE_count=0
declare -i attempt_count=0
declare -i fail_count=0

# $exit_status == 0 means there is no problem
# $exit_status == 1 means the testcase specifier is invalid. This program will exit then.
# $exit_status == 2 means the generator couldn't generate valid testcase because of bad random values.
# In that case, this program doesn't exit but $fail_count will be incremented.

declare output_y # from $your_solution
declare output_n # from $naive_solution

declare -i exit_status_y # from $your_solution
declare -i exit_status_n # from $naive_solution

declare -i previous_count_printed=0
declare -i fail_count_already_printed=0

declare testcase_number_begin
declare testcase_number_end
declare fail_count_to_print

declare stdout_without_whitespaces

# Output of this program will be like:
#
# testcase #   1 - 100 AC
# testcase # 101 - 200 AC (failed to generate: 1)
# testcase # 201 - 265 AC
#
# testcase # 266 WA
# Saved as compere/HH-MM-SS_WA_in_1.txt, compere/HH-MM-SS_WA_out_1.txt
#
# testcase # 267 - 300 AC (failed to generate: 1) < We need to store $fail_count_already_printed
#            ^^^                                    to calculate this value
#            We need to store $previous_count_printed to calculate this value
# ...

function padding () {
  declare ret=$1
  while [ ${#ret} -lt ${#max_number_of_attempts} ]; do
    ret=" ${ret}"
  done
  echo "${ret}"
}

function fail_count_to_string () {
  if [ $1 -eq 0 ]; then
    echo ""
  else
    echo "(failed to generate: $1)"
  fi
}

# Main process
while [ $attempt_count -lt $max_number_of_attempts ]; do
  . <(
    testcase_generator \
      2> >(stderr=$(</dev/stdin); declare -p stderr) \
      1> >(stdout=$(</dev/stdin); declare -p stdout)
    declare -i exit_status=$?
    declare -p exit_status
  )

  # Input file is invalid
  if [ $exit_status -eq 1 ]; then
    printf "%s\n" "$stderr"
    exit 0
  fi

  attempt_count=$(( ++attempt_count ))


  # Failed to generate testcase
  stdout_without_whitespaces=$( echo "${stdout}" | sed -e 's/ //g' -e 's/\n//g' )
  
  if [ -z "${stdout_without_whitespaces}" ] || [ $exit_status -eq 2 ]; then
    fail_count=$(( ++fail_count ))
    if [ $(( attempt_count % 100 )) -eq 0 ]; then
      testcase_number_begin=$( padding $(( previous_count_printed + 1 )) )
      testcase_number_end=$( padding $attempt_count )
      fail_count_to_print=$( fail_count_to_string $(( fail_count - fail_count_already_printed )) )
      printf "testcase #%s - %s \033[32mAC\033[39m %s\n" \
      "${testcase_number_begin}" "${testcase_number_end}" "${fail_count_to_print}"
      fail_count_already_printed=$fail_count
      previous_count_printed=$attempt_count
    fi
    continue
  fi

  # Execute your_solution and store output & exit status
  output_y=$(your_solution <<< $stdout)
  exit_status_y=$?

  # Execute naive_solution and store output & exit status
  output_n=$(naive_solution <<< $stdout)
  exit_status_n=$?

  # RE
  if [ $exit_status_y -gt 0 ] || [ $exit_status_n -gt 0 ]; then
    RE_count=$(( ++RE_count ))

    if [ $(( attempt_count - previous_count_printed )) -ne 1 ]; then
      testcase_number_begin=$( padding $(( previous_count_printed + 1 )) )
      testcase_number_end=$( padding $(( attempt_count - 1 )) )
      fail_count_to_print=$( fail_count_to_string $(( fail_count - fail_count_already_printed )) )
      printf "testcase #%s - %s \033[32mAC\033[39m %s\n\n" \
      "${testcase_number_begin}" "${testcase_number_end}" "${fail_count_to_print}"
      fail_count_already_printed=$fail_count
    fi

    if [ $exit_status_y -gt 0 ] && [ $exit_status_n -gt 0 ]; then # RE (your_solution & naive_solution)
      printf "%s\033[33mRE\033[39m%s #%s\n" \
      "Both of your programs caused a " " on testcase" "${attempt_count}"
      echo "$stdout" > ./compare/$(date +%H-%M-%S)_RE_both_in_${RE_count}.txt
      printf "Saved as %s\n\n" "compare/$(date +%H-%M-%S)_RE_both_in_${RE_count}.txt"
    elif [ $exit_status_y -gt 0 ]; then # RE (your_solution)
      printf "%s\033[33mRE\033[39m%s #%s\n" \
      "'your_solution' caused a " " on testcase" "${attempt_count}"
      echo "$stdout" > ./compare/$(date +%H-%M-%S)_RE_in_${RE_count}.txt
      printf "Saved as %s\n\n" "compare/$(date +%H-%M-%S)_RE_in_${RE_count}.txt"
    elif [ $exit_status_n -gt 0 ]; then # RE (naive_solution)
      printf "%s\033[33mRE\033[39m%s #%s\n" \
      "'naive_solution' caused a " " on testcase" "${attempt_count}"
      echo "$stdout" > ./compare/$(date +%H-%M-%S)_RE_naive_in_${RE_count}.txt
      printf "Saved as %s\n\n" "compare/in_$(date +%H-%M-%S)_RE_naive_${RE_count}.txt"
    fi

    # verbose
    if [ "${1}" == "-v" ] || [ "${1}" == "-vv" ]; then
    printf "\033[35m[input]\033[39m\n%s\n\n" \
    "${stdout}"
    fi

    if [ $(( WA_count + RE_count )) -ge $max_number_of_WA_or_RE ]; then
      break
    fi

    previous_count_printed=$attempt_count
    continue
  fi

  # WA
  if [ "${output_y}" != "${output_n}" ]; then
    WA_count=$(( ++WA_count ))

    if [ $(( attempt_count - previous_count_printed )) -ne 1 ]; then
      testcase_number_begin=$( padding $(( previous_count_printed + 1 )) )
      testcase_number_end=$( padding $(( attempt_count - 1 )) )
      fail_count_to_print=$( fail_count_to_string $(( fail_count - fail_count_already_printed )) )
      printf "testcase #%s - %s \033[32mAC\033[39m %s\n\n" \
      "${testcase_number_begin}" "${testcase_number_end}" "${fail_count_to_print}"
      fail_count_already_printed=$fail_count
    fi
    previous_count_printed=$attempt_count

    printf "testcase #%s \033[31mWA\033[39m\n" "$( padding $attempt_count )"
    echo "$stdout" > ./compare/$(date +%H-%M-%S)_WA_in_${WA_count}.txt
    echo -e "[expected]\n$output_n\n\n[your solution]\n$output_y" > ./compare/$(date +%H-%M-%S)_WA_out_${WA_count}.txt
    printf "Saved as %s, %s\n\n" \
    "compare/$(date +%H-%M-%S)_WA_in_${WA_count}.txt" "compare/$(date +%H-%M-%S)_WA_out_${WA_count}.txt"

    # verbose
    if [ "${1}" == "-v" ] || [ "${1}" == "-vv" ]; then
    printf "\033[35m[input]\033[39m\n%s\n\033[35m[expected]\033[39m\n%s\n\033[35m[your solution]\033[39m\n%s\n\n" \
    "${stdout}" "${output_y}"
    fi

    if [ $(( WA_count + RE_count )) -ge $max_number_of_WA_or_RE ]; then
      break
    fi

    continue
  fi

  # AC
  if [ $(( attempt_count % 100 )) -eq 0 ]; then
    testcase_number_begin=$( padding $(( previous_count_printed + 1 )) )
    testcase_number_end=$( padding $attempt_count )
    fail_count_to_print=$( fail_count_to_string $(( fail_count - fail_count_already_printed )) )
    printf "testcase #%s - %s \033[32mAC\033[39m %s\n" \
    "${testcase_number_begin}" "${testcase_number_end}" "${fail_count_to_print}"
    fail_count_already_printed=$fail_count
    previous_count_printed=$attempt_count

    # verbose
    if [ "${1}" == "-vv" ]; then
    printf "\n\033[35m[input]\033[39m\n%s\n\033[35m[your solution]\033[39m\n%s\n\n" \
    "${stdout}" "${output_y}"
    fi

  fi

done

  if [ "${1}" != "-vv" ] && [ $(( WA_count + RE_count )) -lt $max_number_of_WA_or_RE ]; then
    echo
  fi

function is_or_are () {
  if [ $1 -gt 1 ]; then
    echo "are"
  else
    echo "is"
  fi
}

  printf "\033[36m%s\033[39m attemps have been made. \033[31m${WA_count} WA\033[39m and \033[33m${RE_count} RE\033[39m %s detected.\n" \
  "$(( attempt_count - fail_count ))" "$( is_or_are $(( WA_count + RE_count )) )"
