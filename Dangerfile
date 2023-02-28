# frozen_string_literal: true

URL_SEMANTIC_RELEASE = 'https://www.conventionalcommits.org/en/v1.0.0/#summary'
SEMANTIC_COMMIT_TYPES = %w[build chore ci docs feat fix improvement perf refactor revert style test].freeze

NO_RELEASE = 1
PATCH_RELEASE = 2
MINOR_RELEASE = 3
MAJOR_RELEASE = 4

COMMIT_SUBJECT_MAX_LENGTH = 72

# Commit messages that start with one of the prefixes below won't be linted
IGNORED_COMMIT_MESSAGES = [
  'Merge branch',
  'Revert "'
].freeze

# Perform various checks against commits. We're not using
# https://github.com/jonallured/danger-commit_lint because its output is not
# very helpful, and it doesn't offer the means of ignoring merge commits.

def fail_commit(commit, message)
  fail("#{commit.sha}: #{message}") # rubocop:disable Style/SignalException
end

def warn_commit(commit, message)
  warn("#{commit.sha}: #{message}")
end

def lines_changed_in_commit(commit)
  commit.diff_parent.stats[:total][:lines]
end

def too_many_changed_lines?(commit)
  commit.diff_parent.stats[:total][:files] > 3 &&
    lines_changed_in_commit(commit) >= 250
end

def match_semantic_commit(text)
  text.match(/^(?<type>\w+)(?:\((?<scope>.+?)\))?:(?<description>.+?)$/)
end

def add_no_release_markdown
  markdown(<<~MARKDOWN)
    ## No release

    This Pull Request will trigger _no_ release.
    This either means, no commit warrant a semantic release (e.g. only updating CI config);
    or that all commits are not properly formatted according to [conventional commits](#{URL_SEMANTIC_RELEASE})
    rules, in the latter case, you should rewrite the commits history to format commit
    messages properly
  MARKDOWN
end

def add_release_type_markdown(type)
  markdown(<<~MARKDOWN)
    ## \u{1f4e6} #{type.capitalize} ([conventional commits](#{URL_SEMANTIC_RELEASE}))
  MARKDOWN
end

def get_release_info(release_type)
  case release_type
  when MAJOR_RELEASE
    type = 'major release'
    bump = <<~BUMP
      This will bump the first part of the version number, e.g. `v1.2.3` -> `v2.0.0`.

      This means the changes has a BREAKING CHANGE.
    BUMP
  when MINOR_RELEASE
    type = 'minor release'
    bump = 'This will bump the second part of the version number, e.g. `v1.2.3` -> `v1.3.0`.'
  when PATCH_RELEASE
    type = 'patch release'
    bump = 'This will bump the third part of the version number, e.g. `v1.2.3` -> `v1.2.4`.'
  else
    message 'This PR will trigger no release'
    add_no_release_markdown
    return
  end
  [type, bump]
end

def lint_commit(commit)
  # For now we'll ignore merge commits, as getting rid of those is a problem
  # separate from enforcing good commit messages.
  # We also ignore revert commits as they are well structured by Git already
  if commit.message.start_with?(*IGNORED_COMMIT_MESSAGES)
    return { failed: false, release: NO_RELEASE }
  end

  release = NO_RELEASE
  failures = false
  subject, separator, details = commit.message.split("\n", 3)

  if subject.length > COMMIT_SUBJECT_MAX_LENGTH
    fail_commit(
      commit,
      "The commit subject may not be longer than #{COMMIT_SUBJECT_MAX_LENGTH} characters"
    )

    failures = true
  end

  # Fail if a suggestion commit is used and squash is not enabled
  if commit.message.start_with?('Apply suggestion to') && !github.pr_json['squash']
    fail_commit(
      commit,
      'If you are applying suggestions, squash needs to be enabled in the Pull Request'
    )

    failures = true
  end

  if separator && !separator.empty?
    fail_commit(
      commit,
      'The commit subject and body must be separated by a blank line'
    )

    failures = true
  end

  if !details && too_many_changed_lines?(commit)
    warn_commit(
      commit,
      'Commits that change 250 or more lines across at least three files ' \
        'must describe these changes in the commit body'
    )

    failures = true
  end

  semantic_commit = match_semantic_commit(subject)

  if !semantic_commit
    warn_commit(commit, 'The commit does not comply with conventional commits specifications.')

    failures = true
  elsif !SEMANTIC_COMMIT_TYPES.include?(semantic_commit[:type])
    warn_commit(
      commit,
      "The Semantic commit type `#{semantic_commit[:type]}` is not a well-known semantic commit type."
    )

    failures = true
  elsif details&.match(/BREAKING CHANGE:/)
    release = MAJOR_RELEASE
  elsif semantic_commit[:type] == 'feat'
    release = MINOR_RELEASE
  elsif %w[perf fix].include?(semantic_commit[:type])
    release = PATCH_RELEASE
  end

  { failed: failures, release: release }
end

def lint_commits(commits)
  commits_with_status = commits.map { |commit| { commit: commit }.merge(lint_commit(commit)) }

  failed = commits_with_status.any? { |commit| commit[:failed] }

  max_release = commits_with_status.max { |a, b| a[:release] <=> b[:release] }

  if failed
    markdown(<<~MARKDOWN)
      ## Commit message standards

      One or more commit messages do not meet our Git commit message standards.
      For more information on how to write a good commit message, take a look at
      [Conventional commits](#{URL_SEMANTIC_RELEASE}).

      Here is an example of a good commit message:

          feat(vpc): Adding new outputs

          Added new outputs for the VPC module.

      This is an example of a bad commit message:

          added vpc module

    MARKDOWN
  end

  return if github.pr_json['squash']

  type, bump = get_release_info(max_release[:release])

  if type && bump
    add_release_type_markdown(type)
    markdown(<<~MARKDOWN)
      This Pull Request will trigger a _#{type}_ changes, triggered by commit:
      #{max_release[:commit].sha}

      #{bump}
    MARKDOWN
  end
end

def lint_pr(pr)
  if pr && pr['squash']
    release = NO_RELEASE
    pr_title = pr['title'][/(^WIP: +)?(.*)/, 2]
    semantic_commit = match_semantic_commit(pr_title)

    if !semantic_commit
      warn(
        'Your PR has **Squash commits when Pull Request is accepted** enabled but its title does not comply with conventional commits specifications'
      )

      failures = true
    elsif !SEMANTIC_COMMIT_TYPES.include?(semantic_commit[:type])
      warn(
        "The Semantic commit type `#{semantic_commit[:type]}` is not a well-known semantic commit type."
      )

      failures = true
    elsif semantic_commit[:type] == 'feat'
      release = MINOR_RELEASE
    elsif %w[perf fix].include?(semantic_commit[:type])
      release = PATCH_RELEASE
    end

    type, bump = get_release_info(release)

    if type && bump
      add_release_type_markdown(type)
      markdown(<<~MARKDOWN)
        This Pull Request will trigger a _#{type}_ changes based on its title.

        #{bump}
      MARKDOWN
    end
  end
end

lint_commits(git.commits)
lint_pr(github.pr_json)

if git.commits.length > 10
  warn(
    'This Pull Request includes more than 10 commits. ' \
      'Please rebase these commits into a smaller number of commits.'
  )
end
