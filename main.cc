#include <algorithm>
#include <iostream>
#include <limits>
#include <map>
#include <random>
#include <string>
#include <type_traits>
#include <utility>
#include <variant>
#include <vector>

#ifdef LOCAL
#define debug_print std::cerr << __func__ << " " << __LINE__ << std::endl
#define dmp(x) std::cerr << #x << ": " << x << std::endl;
#else
#define debug_print ((void) 0)
#define dmp(x) ((void) 0)
#endif

constexpr int NOT_SET = std::numeric_limits<int>::max();
static std::map<std::string, int> ID;  // Convert variable names into IDs

class variable;
static std::vector<variable> Vars;

long long convert_to_integer(const std::string &s) {
  /*
    This function converts a string into an integer.
    If the input is not an integer, this function
    returns NOT_SET.
  */
  long long ret = 0;
  int idx = static_cast<int>(s.front() == '-');

  for (; idx < static_cast<int>(s.size()); idx++) {
    if (s[idx] < '0' || s[idx] > '9') return NOT_SET;
    ret *= 10;
    ret += s[idx] - '0';
  }

  if (s.front() == '-') ret *= -1;
  return ret;
}

[[noreturn]] void invalid_input_error(const std::string &error_msg) {
  std::cerr << "[Error] " << error_msg << std::endl;
  exit(1);
}

[[noreturn]] void no_value_error() {
  std::cerr << "[Error] "
            << "There is no value which satisfies the restrictions." << std::endl;
  exit(2);
}

static std::random_device rd;

template <class T>
T random_integer(T low, T high) {
  if (low > high) no_value_error();
  if (low == high) return low;

  std::mt19937_64 mt(rd());
  std::uniform_int_distribution<T> dist(low, high);
  return dist(mt);
}

enum compare {
  NOT_EQUAL_TO = 0,
  GREATER_THAN = 1,
  GREATER_THAN_OR_EQUAL_TO = 2,
  LESS_THAN = 3,
  LESS_THAN_OR_EQUAL_TO = 4,
};

struct integer_variable_info {
  /*
    `min` and `max` are integers that represents
    minimum/maximum value of this variable.

    These values can also be specified by another variable.
  */
  long long min;
  long long min_var_id;
  long long min_offset;

  long long max;
  long long max_var_id;
  long long max_offset;

  /*
    Options

    `condition_var` specifies the ID of another variable.

    `condition` is an integer between 0 to 4.
    0: This variable must not be equal to the variable `condition_var`.
    1: This variable must be grater than the variable `condition_var`.
    2: This variable must be grater than or equal to the variable `condition_var`.
    3: This variable must be less than the variable `condition_var`.
    4: This variable must be less than or equal to the variable `condition_var`.

    `remainder` and `mod` are also integers.
    `actual_value` is the actual (generated) value of this variable.
    Divided by `mod`, `actual_value` must leaves a remainder of `remainder`.
  */
  int condition_var;
  int condition;

  long long remainder;
  long long mod;

  std::vector<long long> actual_value;
};

struct string_variable_info {
  /*
    `len_min` and `len_max` are integers that
    represent minimun/maximum string length.

    The length can also be specified by another variable.
  */
  int len_min;
  int len_min_var_id;
  int len_min_offset;

  int len_max;
  int len_max_var_id;
  int len_max_offset;

  /* The string consists of the characters in `characters_allowed`. */
  std::vector<char> characters_allowed;

  /*
    Options

    `condition_var` specifies the ID of another variable.

    `condition` is an integer between 0 to 4.
    0: This variable must not be equal to the variable `condition_var`.
    1: This variable must be grater than the variable `condition_var`.
    2: This variable must be grater than or equal to the variable `condition_var`.
    3: This variable must be less than the variable `condition_var`.
    4: This variable must be less than or equal to the variable `condition_var`.

    Lexicographic order is used to compare strings.
  */
  int condition_var;
  int condition;

  std::vector<std::string> actual_value;
};

class variable {
  /* Member variables */
  std::variant<integer_variable_info, string_variable_info> info;

  /*
    `size` is an integer that represents vector size.
    Note that an integer or a string is also treated as a vector (of size 1).

    The size is often specified by another variable.
    In that case, the ID of that variable is stored
    `size_var_id` and `size` is set to be NOT_SET.

    `size_offset` specifies the difference between
    the actual size of this vector and `size_var_id.info.actual_value`.
  */
  int size_var_id;
  int size_offset;

 public:
  int size;
  bool printed_horizontally;

  /* Constructors */
  // Constructor for an integer variable
  variable(const bool &horizontal,
           const std::string &size_scanned, const int &size_offset_scanned,
           const std::string &min_scanned, const long long &min_offset_scanned,
           const std::string &max_scanned, const long long &max_offset_scanned,
           const std::string &comp_option_scanned, const std::string &mod_option_scanned) {
    // Set variable type
    printed_horizontally = horizontal;
    info = integer_variable_info();
    is_integer = true;

    generated = false;
    compiled = false;

    integer_variable_info &this_var = std::get<integer_variable_info>(this->info);

    // Set vector size
    if (const int size_scanned_to_integer = static_cast<int>(convert_to_integer(size_scanned));
        size_scanned_to_integer == NOT_SET) {
      if (ID.count(size_scanned) == 0) {
        debug_print;
        invalid_input_error("Variable called '" + size_scanned + "' has not been declared.");
      } else {
        this->size = NOT_SET;
        this->size_var_id = ID[size_scanned];
        this->size_offset = size_offset_scanned;
      }
    } else {
      this->size = size_scanned_to_integer;
      this->size_var_id = NOT_SET;
      this->size_offset = size_offset_scanned;
    }

    // Set minimum value
    if (const long long min_scanned_to_integer = convert_to_integer(min_scanned);
        min_scanned_to_integer == NOT_SET) {
      if (ID.count(min_scanned) == 0) {
        debug_print;
        invalid_input_error("Variable called '" + min_scanned + "' has not been declared.");
      } else {
        this_var.min = NOT_SET;
        this_var.min_var_id = ID[min_scanned];
        this_var.min_offset = min_offset_scanned;
      }
    } else {
      this_var.min = min_scanned_to_integer;
      this_var.min_var_id = NOT_SET;
      this_var.min_offset = min_offset_scanned;
    }

    // Set maximum value
    if (const long long max_scanned_to_integer = convert_to_integer(max_scanned);
        max_scanned_to_integer == NOT_SET) {
      if (ID.count(max_scanned) == 0) {
        debug_print;
        invalid_input_error("Variable called '" + max_scanned + "' has not been declared.");
      } else {
        this_var.max = NOT_SET;
        this_var.max_var_id = ID[max_scanned];
        this_var.max_offset = max_offset_scanned;
      }
    } else {
      this_var.max = max_scanned_to_integer;
      this_var.max_var_id = NOT_SET;
      this_var.max_offset = max_offset_scanned;
    }

    // Set compare options
    if (comp_option_scanned != "") {
      // Parse input
      int condition;
      std::string condition_var;

      if (comp_option_scanned[0] == '!' && comp_option_scanned[1] == '=') {
        condition = NOT_EQUAL_TO;
        condition_var = comp_option_scanned.substr(2);
      } else if (comp_option_scanned[0] == '>' && comp_option_scanned[1] != '=') {
        condition = GREATER_THAN;
        condition_var = comp_option_scanned.substr(1);
      } else if (comp_option_scanned[0] == '>') {
        condition = GREATER_THAN_OR_EQUAL_TO;
        condition_var = comp_option_scanned.substr(2);
      } else if (comp_option_scanned[0] == '<' && comp_option_scanned[1] != '=') {
        condition = LESS_THAN;
        condition_var = comp_option_scanned.substr(1);
      } else if (comp_option_scanned[0] == '<') {
        condition = LESS_THAN_OR_EQUAL_TO;
        condition_var = comp_option_scanned.substr(2);
      } else {
        debug_print;
        invalid_input_error("Inequality sign must be '!=', '>', '>=', '<' or '<='.");
      }

      if (ID.count(condition_var) == 0) {
        debug_print;
        invalid_input_error("Variable called '" + condition_var + "' has not been declared.");
      }

      this_var.condition = condition;
      this_var.condition_var = ID[condition_var];
    } else {
      this_var.condition_var = NOT_SET;
      this_var.condition = NOT_SET;
    }

    // Set mod options
    if (mod_option_scanned != "") {
      int persent_idx = -1;
      for (int idx = 0; idx < static_cast<int>(mod_option_scanned.size()); idx++) {
        if (mod_option_scanned[idx] == '%') {
          persent_idx = idx;
          break;
        }
      }

      if (persent_idx == -1) {
        debug_print;
        invalid_input_error("Invalid mod option (mod option must be like '1%2')");
      }

      const long long remainder = convert_to_integer(mod_option_scanned.substr(0, persent_idx));
      const long long mod = convert_to_integer(mod_option_scanned.substr(persent_idx + 1));

      if (remainder == NOT_SET || mod == NOT_SET) {
        debug_print;
        invalid_input_error("Invalid mod option (mod option must be like '1%2')");
      }

      std::get<integer_variable_info>(this->info).remainder = remainder;
      std::get<integer_variable_info>(this->info).mod = mod;
    } else {
      std::get<integer_variable_info>(this->info).remainder = NOT_SET;
      std::get<integer_variable_info>(this->info).mod = NOT_SET;
    }
  }

  // Constructor for a string variable
  variable(const bool &horizontal,
           const std::string &size_scanned, const int &size_offset_scanned,
           const std::string &len_min_scanned, const int &len_min_offset_scanned,
           const std::string &len_max_scanned, const int &len_max_offset_scanned,
           const std::vector<char> &characters_scanned, const std::string &comp_option_scanned) {
    // Set variable type
    printed_horizontally = horizontal;
    info = string_variable_info();
    is_integer = false;

    generated = false;
    compiled = false;

    string_variable_info &this_var = std::get<string_variable_info>(this->info);

    // Set vector size
    if (const int size_scanned_to_integer = static_cast<int>(convert_to_integer(size_scanned));
        size_scanned_to_integer == NOT_SET) {
      if (ID.count(size_scanned) == 0) {
        debug_print;
        invalid_input_error("Variable called '" + size_scanned + "' has not been declared.");
      } else {
        this->size = NOT_SET;
        this->size_var_id = ID[size_scanned];
        this->size_offset = size_offset_scanned;
      }
    } else {
      this->size = size_scanned_to_integer;
      this->size_var_id = NOT_SET;
      this->size_offset = size_offset_scanned;
    }

    // Set characters to use
    if (characters_scanned.empty()) {
      debug_print;
      invalid_input_error("Please specify characters of which your string consist.");
    } else
      this_var.characters_allowed = characters_scanned;

    // Set minimum string length
    if (const int len_min_scanned_to_integer = static_cast<int>(convert_to_integer(len_min_scanned));
        len_min_scanned_to_integer == NOT_SET) {
      if (ID.count(len_min_scanned) == 0) {
        debug_print;
        invalid_input_error("Variable called '" + len_min_scanned + "' has not been declared.");
      } else {
        this_var.len_min = NOT_SET;
        this_var.len_min_var_id = ID[len_min_scanned];
        this_var.len_min_offset = len_min_offset_scanned;
      }
    } else {
      this_var.len_min = len_min_scanned_to_integer;
      this_var.len_min_var_id = NOT_SET;
      this_var.len_min_offset = len_min_offset_scanned;
    }

    // Set maximum string length
    if (const int len_max_scanned_to_integer = static_cast<int>(convert_to_integer(len_max_scanned));
        len_max_scanned_to_integer == NOT_SET) {
      if (ID.count(len_max_scanned) == 0) {
        debug_print;
        invalid_input_error("Variable called '" + len_max_scanned + "' has not been declared.");
      } else {
        this_var.len_max = NOT_SET;
        this_var.len_max_var_id = ID[len_max_scanned];
        this_var.len_max_offset = len_max_offset_scanned;
      }
    } else {
      this_var.len_max = len_max_scanned_to_integer;
      this_var.len_max_var_id = NOT_SET;
      this_var.len_max_offset = len_max_offset_scanned;
    }

    // Set compare options
    if (comp_option_scanned != "") {
      // Parse input
      int condition;
      std::string condition_var;

      if (comp_option_scanned[0] == '!' && comp_option_scanned[1] == '=') {
        condition = NOT_EQUAL_TO;
        condition_var = comp_option_scanned.substr(2);
      } else if (comp_option_scanned[0] == '>' && comp_option_scanned[1] != '=') {
        condition = GREATER_THAN;
        condition_var = comp_option_scanned.substr(1);
      } else if (comp_option_scanned[0] == '>') {
        condition = GREATER_THAN_OR_EQUAL_TO;
        condition_var = comp_option_scanned.substr(2);
      } else if (comp_option_scanned[0] == '<' && comp_option_scanned[1] != '=') {
        condition = LESS_THAN;
        condition_var = comp_option_scanned.substr(1);
      } else if (comp_option_scanned[0] == '<') {
        condition = LESS_THAN_OR_EQUAL_TO;
        condition_var = comp_option_scanned.substr(2);
      } else {
        debug_print;
        invalid_input_error("Inequality sign must be '!=', '>', '>=', '<' or '<='.");
      }

      if (ID.count(condition_var) == 0) {
        debug_print;
        invalid_input_error("Variable called '" + condition_var + "' has not been declared.");
      }

      this_var.condition = condition;
      this_var.condition_var = ID[condition_var];
    } else {
      this_var.condition_var = NOT_SET;
      this_var.condition = NOT_SET;
    }
  }

  bool is_integer;

  /* Member functions */
  long long integer_value(int idx = 0) {
    if (!generated) generate();
    if (idx >= this->size)
      return std::get<integer_variable_info>(this->info).actual_value[0];
    else
      return std::get<integer_variable_info>(this->info).actual_value[idx];
  }

  std::string string_value(int idx = 0) {
    if (!generated) generate();
    if (idx >= this->size)
      return std::get<string_variable_info>(this->info).actual_value[0];
    else
      return std::get<string_variable_info>(this->info).actual_value[idx];
  }

  // Generate random values
  void generate() {
    if (generated) return;
    if (!compiled) compile();

    if (is_integer) {  // Generate integers
      integer_variable_info &this_var = std::get<integer_variable_info>(this->info);

      for (int idx = 0; idx < (this->size); idx++) {
        long long &ret = this_var.actual_value[idx];

        if (this_var.mod == NOT_SET) {  // If there is no mod option
          long long low = this_var.min;
          long long high = this_var.max;

          // Restrict minimum value
          if (this_var.condition == GREATER_THAN)
            low = std::max(low, Vars[this_var.condition_var].integer_value(idx)) + 1;
          if (this_var.condition == GREATER_THAN_OR_EQUAL_TO)
            low = std::max(low, Vars[this_var.condition_var].integer_value(idx));

          // Restrict maximum value
          if (this_var.condition == LESS_THAN)
            high = std::min(high, Vars[this_var.condition_var].integer_value(idx) - 1);
          if (this_var.condition == LESS_THAN_OR_EQUAL_TO)
            high = std::min(high, Vars[this_var.condition_var].integer_value(idx));

          if (this_var.condition == NOT_EQUAL_TO && low == high && low == Vars[this_var.condition_var].integer_value(idx))
            no_value_error();

          do {
            ret = random_integer(low, high);
          } while (
              this_var.condition == NOT_EQUAL_TO && ret == Vars[this_var.condition_var].integer_value(idx)
              // Roll a dice again (if necessary)
          );
        } else {  // If mod option is specified
          long long low = this_var.min;
          long long high = this_var.max;

          // Restrict minimum value
          if (this_var.condition == GREATER_THAN)
            low = std::max(low, Vars[this_var.condition_var].integer_value(idx) + 1);
          else if (this_var.condition == GREATER_THAN_OR_EQUAL_TO)
            low = std::max(low, Vars[this_var.condition_var].integer_value(idx));

          // Restrict maximum value
          if (this_var.condition == LESS_THAN)
            high = std::min(high, Vars[this_var.condition_var].integer_value(idx) - 1);
          else if (this_var.condition == LESS_THAN_OR_EQUAL_TO)
            high = std::min(high, Vars[this_var.condition_var].integer_value(idx));

          // Modify low & high values to make them satisfy the mod option
          {
            const long long rem = ((low < 0) ? (low % this_var.mod + this_var.mod) : (low % this_var.mod));
            if (rem > this_var.remainder)
              low += this_var.mod + this_var.remainder - rem;
            else if (rem < this_var.remainder)
              low += this_var.remainder - rem;
          }
          {
            const long long rem = ((high < 0) ? (high % this_var.mod + this_var.mod) : (high % this_var.mod));
            if (rem > this_var.remainder)
              high -= rem - this_var.remainder;
            else if (rem < this_var.remainder)
              high -= rem - this_var.remainder + this_var.mod;
          }

          // There are `cnt` + 1 possible values
          const long long cnt = (high - low) / this_var.mod;

          if (this_var.condition == NOT_EQUAL_TO && cnt == 0 && low == Vars[this_var.condition_var].integer_value(idx))
            no_value_error();

          do {
            ret = random_integer(0LL, cnt) * this_var.mod + low;
          } while (
              this_var.condition == NOT_EQUAL_TO && ret == Vars[this_var.condition_var].integer_value(idx)
              // Roll a dice again (if necessary)
          );
        }
      }
    } else {  // Generate strings
      string_variable_info &this_var = std::get<string_variable_info>(this->info);

      for (int idx = 0; idx < (this->size); idx++) {
        std::string &ret = this_var.actual_value[idx];

        // Generate string length
        const int len = random_integer(this_var.len_min, this_var.len_max);
        ret.resize(len);

        bool comp_option_satisfied = false;

        while (!comp_option_satisfied) {
          for (int char_idx = 0; char_idx < len; char_idx++)
            ret[char_idx] = this_var.characters_allowed[random_integer(0, static_cast<int>(this_var.characters_allowed.size()) - 1)];

          switch (this_var.condition) {
            case NOT_SET:
              comp_option_satisfied = true;
              break;
            case NOT_EQUAL_TO:
              comp_option_satisfied = (ret != Vars[this_var.condition_var].string_value(idx));
              break;
            case GREATER_THAN:
              comp_option_satisfied = (ret > Vars[this_var.condition_var].string_value(idx));
              break;
            case GREATER_THAN_OR_EQUAL_TO:
              comp_option_satisfied = (ret >= Vars[this_var.condition_var].string_value(idx));
              break;
            case LESS_THAN:
              comp_option_satisfied = (ret < Vars[this_var.condition_var].string_value(idx));
              break;
            case LESS_THAN_OR_EQUAL_TO:
              comp_option_satisfied = (ret <= Vars[this_var.condition_var].string_value(idx));
              break;
          }
        }
      }
    }

    generated = true;
  }

 private:
  bool generated, compiled;

  // Set actual values of size, min, max, etc. if NOT_SET
  void compile() {
    if (compiled) return;

    if (is_integer) {
      integer_variable_info &this_var = std::get<integer_variable_info>(this->info);

      if (this->size == NOT_SET)
        this->size = static_cast<int>(Vars[this->size_var_id].integer_value()) + this->size_offset;
      if (this_var.min == NOT_SET)
        this_var.min = Vars[this_var.min_var_id].integer_value() + this_var.min_offset;
      if (this_var.max == NOT_SET)
        this_var.max = Vars[this_var.max_var_id].integer_value() + this_var.max_offset;

      // Set vector size
      this_var.actual_value = std::vector<long long>(this->size, NOT_SET);
    } else {
      string_variable_info &this_var = std::get<string_variable_info>(this->info);

      if (this->size == NOT_SET)
        this->size = static_cast<int>(Vars[this->size_var_id].integer_value()) + this->size_offset;
      if (this_var.len_min == NOT_SET)
        this_var.len_min = static_cast<int>(Vars[this_var.len_min_var_id].integer_value()) + this_var.len_min_offset;
      if (this_var.len_max == NOT_SET)
        this_var.len_max = static_cast<int>(Vars[this_var.len_max_var_id].integer_value()) + this_var.len_max_offset;

      // Set vector size
      this_var.actual_value = std::vector<std::string>(this->size, "");
    }

    compiled = true;
  }
};

std::pair<std::string, std::string> parse_type_options(const std::string &type, const std::string &var_name) {
  // Search for round parenthesis
  /*
    option_begin_idx is the index of '('
    option_end_idx is the index of ')'
  */

  int option_begin_idx = -1, option_end_idx = -1;
  for (int idx = 3; idx < static_cast<int>(type.size()); idx++) {
    if (type[idx] == '(') {
      if (option_begin_idx == -1)
        option_begin_idx = idx;
      else {
        debug_print;
        invalid_input_error("'(' is duplicated in type specifier of '" + var_name + "'.");
      }
    }

    if (type[idx] == ')') {
      if (option_begin_idx == -1) {
        debug_print;
        invalid_input_error("')' comes before '(' in type specifier of '" + var_name + "'.");
      } else if (option_end_idx != -1) {
        debug_print;
        invalid_input_error("')' is duplicated in type specifier of '" + var_name + "'.");
      } else
        option_end_idx = idx;
    }
  }

  /*
    options should be like: "!=N,1%2" ">= N, 1 % 2" ">=N" ",1%2"
  */
  std::string options;
  if (option_begin_idx == -1)
    options = "";
  else if (option_end_idx == -1) {
    debug_print;
    invalid_input_error("')' is missing in type specifier of '" + var_name + "'.");
  } else
    options = type.substr(option_begin_idx + 1, option_end_idx - option_begin_idx - 1);

  /*
    ret.first  should be like: "!=N" ">N" "<=N"
    ret.second should be like: "1%2" "0%2" "5%13"
  */
  std::pair<std::string, std::string> ret = {"", ""};
  std::string &comp_option = ret.first;
  std::string &mod_option = ret.second;

  if (options != "") {
    // Search for comma
    int comma_idx = -1;
    for (int idx = 0; idx < static_cast<int>(options.size()); idx++) {
      if (options[idx] == ',') {
        comma_idx = idx;
        break;
      }
    }

    if (comma_idx == -1) {  // has a comp option && does not have mod options
      comp_option.reserve(options.size());
      for (int idx = 0; idx < static_cast<int>(options.size()); idx++) {
        comp_option.push_back(options[idx]);
      }
    } else if (comma_idx == 0) {  // does not have comp options && has a mod option
      mod_option.reserve(options.size());
      for (int idx = 1 /* because options[0] == ',' */; idx < static_cast<int>(options.size()); idx++) {
        mod_option.push_back(options[idx]);
      }
    } else {  // has a comp option && has a mod option
      comp_option.reserve(options.size());
      mod_option.reserve(options.size());

      for (int idx = 0; idx < comma_idx; idx++) {
        comp_option.push_back(options[idx]);
      }

      for (int idx = comma_idx + 1; idx < static_cast<int>(options.size()); idx++) {
        mod_option.push_back(options[idx]);
      }
    }
  }

  return ret;
}

std::pair<std::string, long long> parse_limit_options(const std::string &var_name, const std::string &section_name) {
  std::string value;
  std::cin >> value;

  /*
    Case 1: If `value` is a number (e.g. "30"), this function returns { "30", 0 }
    Case 2: If `value` is a variable (e.g. "N"), this function returns { "N", 0 }
    Case 3: If `value` is a veriable with offset (e.g. "N(-1)"), this function returns { "N", -1 }
  */

  // Search for round parenthesis
  /*
    offset_begin_idx is the index of '('
    offset_end_idx is the index of ')'
  */
  int offset_begin_idx = -1, offset_end_idx = -1;

  for (int idx = 1; idx < static_cast<int>(value.size()); idx++) {
    if (value[idx] == '(') {
      if (offset_begin_idx == -1)
        offset_begin_idx = idx;
      else {
        debug_print;
        invalid_input_error("'(' is duplicated in " + section_name + " of " + var_name + ".");
      }
    }

    if (value[idx] == ')') {
      if (offset_begin_idx == -1) {
        debug_print;
        invalid_input_error("')' comes before '(' in " + section_name + " of " + var_name + ".");
      } else if (offset_end_idx != -1) {
        debug_print;
        invalid_input_error("')' is duplicated in " + section_name + " of " + var_name + ".");
      } else
        offset_end_idx = idx;
    }
  }

  if (offset_begin_idx == -1 && offset_end_idx == -1)  // Case 1 or Case 2
    return {value, 0};
  else if (offset_end_idx != -1) {  // Case 3
    long long offset = convert_to_integer(value.substr(offset_begin_idx + 1, offset_end_idx - offset_begin_idx - 1));
    if (offset == NOT_SET) {
      debug_print;
      invalid_input_error("Offset of " + section_name + " of '" + var_name + "' must be an integer.");
    }
    return {value.substr(0, offset_begin_idx), offset};
  } else {  // Error
    debug_print;
    invalid_input_error(section_name + " of '" + var_name + "' is invalid.");
  }
}

variable parse_int(bool printed_horizontally,
                   const std::string &var_name,
                   const std::string &type,
                   const std::string &vector_size,
                   int vector_size_offset) {
  // Process typename
  std::pair<std::string, std::string> type_options = parse_type_options(type, var_name);

  // Process minimum values
  std::pair<std::string, long long> min_options = parse_limit_options(var_name, "minimum value");

  // Process maximum values
  std::pair<std::string, long long> max_options = parse_limit_options(var_name, "maximum value");

  return variable{
      printed_horizontally,  // printed horizontally
      vector_size,           // vector size
      vector_size_offset,    // vector size offset
      min_options.first,     // minimum value (or variable name)
      min_options.second,    // minimum value offset
      max_options.first,     // maximum value (or variable name)
      max_options.second,    // maximum value offset
      type_options.first,    // compare options
      type_options.second    // mod options
  };
}

variable parse_string(bool printed_horizontally,
                      const std::string &var_name,
                      const std::string &type,
                      const std::string &vector_size,
                      int vector_size_offset) {
  /* Process typename */

  // Search for square brackets
  int bracket_open_idx = -1, bracket_close_idx = -1;
  for (int idx = 3; idx < static_cast<int>(type.size()); idx++) {
    if (type[idx] == '[') {
      if (bracket_open_idx == -1)
        bracket_open_idx = idx;
      else {
        debug_print;
        invalid_input_error("'[' is duplicated in characters specifier of " + var_name + ".");
      }
    }

    if (type[idx] == ']') {
      if (bracket_open_idx == -1) {
        debug_print;
        invalid_input_error("']' comes before '(' at characters specifier of " + var_name + ".");
      } else if (bracket_close_idx != -1) {
        debug_print;
        invalid_input_error("']' is duplicated in characters specifier of " + var_name + ".");
      } else
        bracket_close_idx = idx;
    }
  }

  if (bracket_open_idx == -1 || bracket_close_idx == -1) {
    debug_print;
    invalid_input_error("Please specify characters of which '" + var_name + "' consist.");
  }

  // Search for comma
  std::vector<int> comma_idx = {bracket_open_idx};
  for (int idx = bracket_open_idx + 1; idx < bracket_close_idx; idx++) {
    if (type[idx] == ',') comma_idx.emplace_back(idx);
  }
  comma_idx.emplace_back(bracket_close_idx);

  std::vector<char> characters;

  for (int range = 0; range < static_cast<int>(comma_idx.size()) - 1; range++) {
    const std::string::const_iterator range_begin = type.cbegin() + comma_idx[range] + 1;
    const std::string::const_iterator range_end = type.cbegin() + comma_idx[range + 1];

    if (const long hyphens = std::count(range_begin, range_end, '-'); hyphens == 1) {  // If there is a hyphen
      char begin = '\0', end = '\0';
      for (int idx = comma_idx[range] + 1; idx < comma_idx[range + 1]; idx++) {
        if (type[idx] == '-')
          continue;
        else if (begin == '\0')
          begin = type[idx];
        else if (end == '\0')
          end = type[idx];
        else {
          debug_print;
          invalid_input_error("Characters specifier of '" + var_name + "' is invalid.");
        }
      }
      if (begin == '\0' || end == '\0' || begin > end) {
        debug_print;
        invalid_input_error("Characters specifier of '" + var_name + "' is invalid.");
      }

      // Add characters
      for (char c = begin; c <= end; c++) characters.emplace_back(c);
    } else if (hyphens == 0) {  // There is no hyphen
      // Add characters
      for (int idx = comma_idx[range] + 1; idx < comma_idx[range + 1]; idx++) {
        characters.emplace_back(type[idx]);
      }
    } else {  // There are more than 1 hyphen
      debug_print;
      invalid_input_error("Characters specifier of '" + var_name + "' is invalid.");
    }
  }

  // Ensure that the vector is distinct
  std::sort(characters.begin(), characters.end());
  characters.erase(std::unique(characters.begin(), characters.end()), characters.end());

  std::string comp_option = parse_type_options(type, var_name).first;

  // Process minimum length
  const std::pair<std::string, long long> len_min_options = parse_limit_options(var_name, "minimum string length");

  // Process maximum length
  const std::pair<std::string, long long> len_max_options = parse_limit_options(var_name, "maximum string length");

  return variable{
      printed_horizontally,                      // printed horizontally
      vector_size,                               // vector size
      vector_size_offset,                        // vector size offset
      len_min_options.first,                     // minimum length (or variable name)
      static_cast<int>(len_min_options.second),  // minimum length offset
      len_max_options.first,                     // maximum length (or variable name)
      static_cast<int>(len_max_options.second),  // maximum length offset
      characters,                                // allowed characters
      comp_option                                // compare options
  };
}

int main() {
  /*
    Check if the input starts with the word
    "variable" in case you feed a wrong text file.
  */
  {
    std::string starts_with;
    std::cin >> starts_with;
    if (starts_with != "variable") {
      debug_print;
      invalid_input_error("Input must start with the word 'variable'.");
    }
  }

  /* Scan variable information */
  while (true) {
    // Process variable names
    std::string var_name;
    std::cin >> var_name;
    if (var_name == "format") break;

    if (ID.count(var_name) != 0) {
      debug_print;
      invalid_input_error("Variable called '" + var_name + "' has already been declared.");
    }

    ID[var_name] = static_cast<int>(Vars.size());

    // Process type specifiers
    std::string type;
    std::cin >> type;

    if (const std::string basetype = type.substr(0, 3); basetype == "int")
      Vars.emplace_back(parse_int(true, var_name, type, "1", 0));
    else if (basetype == "str") {
      Vars.emplace_back(parse_string(true, var_name, type, "1", 0));
    } else if (basetype == "vec" && (type[3] == 'h' || type[3] == 'v')) {
      const std::pair<std::string, long long> size_options = parse_limit_options(var_name, "vector size");

      std::string elem_type;
      std::cin >> elem_type;

      if (std::string base_elem_type = elem_type.substr(0, 3); base_elem_type == "int")
        Vars.emplace_back(parse_int((type[3] == 'h'), var_name, elem_type, size_options.first, static_cast<int>(size_options.second)));
      else if (base_elem_type == "str")
        Vars.emplace_back(parse_string((type[3] == 'h'), var_name, elem_type, size_options.first, static_cast<int>(size_options.second)));
      else {
        debug_print;
        invalid_input_error("Elements of a vector must be 'int' or 'str'.");
      }

    } else {
      debug_print;
      invalid_input_error("Variable type must be 'int', 'str', 'vech' or 'vecv'.");
    }
  }

  /* Generate random values */
  for (int var_ID = 0; var_ID < static_cast<int>(Vars.size()); var_ID++)
    Vars[var_ID].generate();

  /* Scan format information */
  std::vector<std::vector<int>> to_be_printed;  // to_be_printed[i] contains IDs of variables printed in line i
  std::string line_scanned;                     // getline

  while (std::getline(std::cin, line_scanned)) {
    // Remove newline characters and add single whitespace
    if (line_scanned.size() > 0 && line_scanned.back() == '\n')
      line_scanned.pop_back();
    if (line_scanned.size() > 0 && line_scanned.back() == '\r')
      line_scanned.pop_back();
    if (line_scanned.size() == 0) continue;
    line_scanned += ' ';

    to_be_printed.emplace_back();
    int prev_whitespace_idx = -1;

    for (int pos = 0; pos < static_cast<int>(line_scanned.size()); pos++) {
      if (line_scanned[pos] == ' ') {
        const std::string var_name = line_scanned.substr(prev_whitespace_idx + 1, pos - prev_whitespace_idx - 1);
        if (ID.count(var_name) == 0)
          invalid_input_error("Variable called '" + var_name + "' has not been declared.");

        to_be_printed.back().emplace_back(ID[var_name]);
        prev_whitespace_idx = pos;
      }
    }
  }

  /* Print values */
  for (int line = 0; line < static_cast<int>(to_be_printed.size()); line++) {
    if (Vars[to_be_printed[line].front()].printed_horizontally) {  // Horizontally
      for (int idx_in_line = 0; idx_in_line < static_cast<int>(to_be_printed[line].size()); idx_in_line++) {
        const int &var_ID = to_be_printed[line][idx_in_line];
        if (Vars[var_ID].is_integer) {
          for (int idx_in_a_variable = 0; idx_in_a_variable < Vars[var_ID].size; idx_in_a_variable++) {
            std::cout << Vars[var_ID].integer_value(idx_in_a_variable)
                      << (idx_in_line == static_cast<int>(to_be_printed[line].size()) - 1 ? " " : "");
          }
        } else {
          for (int idx_in_a_variable = 0; idx_in_a_variable < Vars[var_ID].size; idx_in_a_variable++) {
            std::cout << Vars[var_ID].string_value(idx_in_a_variable)
                      << (idx_in_line == static_cast<int>(to_be_printed[line].size()) - 1 ? " " : "");
          }
        }
        std::cout << " \n"[idx_in_line == static_cast<int>(to_be_printed[line].size()) - 1];
      }
    } else {  // Vertically
      const int &front_var_ID = to_be_printed[line].front();
      for (int line_cnt = 0; line_cnt < Vars[front_var_ID].size; line_cnt++) {
        for (int idx_in_line = 0; idx_in_line < static_cast<int>(to_be_printed[line].size()); idx_in_line++) {
          const int &var_ID = to_be_printed[line][idx_in_line];
          if (Vars[var_ID].is_integer)
            std::cout << Vars[var_ID].integer_value(line_cnt)
                      << " \n"[idx_in_line == static_cast<int>(to_be_printed[line].size()) - 1];
          else
            std::cout << Vars[var_ID].string_value(line_cnt)
                      << " \n"[idx_in_line == static_cast<int>(to_be_printed[line].size()) - 1];
        }
      }
    }
  }
}
