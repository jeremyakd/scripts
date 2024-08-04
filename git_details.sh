# Define the function
function ll_with_git_info() {
  # Define color codes
  local blue_bold='\033[1;34m'
  local orange='\033[1;33m'
  local red_circle='\033[1;31m●\033[0m'
  local green_bold='\033[1;32m'
  local reset='\033[0m'
  local commit='\033[1;35m'

  # Capture the output of ls -l
  local output
  output=$(ls -l --group-directories-first "$@")

  # Iterate over lines of ls output
  while IFS= read -r line; do
    # Extract directory name
    if [[ $line =~ ^d ]]; then
      dir=$(echo "$line" | awk '{print $NF}')
      # Check if it's a git repository
      if [ -d "$dir/.git" ]; then
        # Get current branch
        branch=$(git -C "$dir" rev-parse --abbrev-ref HEAD)
        # Check for uncommitted changes
        if git -C "$dir" diff --quiet --ignore-submodules HEAD; then
          changes=""
        else
          changes=" $red_circle"
        fi

        # Get the date of the last commit in the format dd/mm/yyyy
        last_commit_date=$(git -C "$dir" log -1 --format=%cd --date=format:'%d/%m/%Y')
        # Get the short hash of the last commit
        last_commit_hash=$(git -C "$dir" log -1 --format=%h)

        # Print the original line with the branch, changes, and last commit date appended, colored in blue and bold
        echo "${line/$dir/$blue_bold$dir$reset} ${orange}(${branch}${changes}${orange})${reset} ${green_bold}->${reset} ${commit}${last_commit_hash}${reset} - ${last_commit_date}"
      else
        # Print the original line, colored in blue and bold for directories
        echo "${line/$dir/$blue_bold$dir$reset}"
      fi
    else
      # Print the original line if it's not a directory
      echo "$line"
    fi
  done <<< "$output"
}

# Create an alias for the function
alias ll='ll_with_git_info'
