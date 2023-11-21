# Warn if scheduled workflow is about to be disabled

> To prevent unnecessary workflow runs, scheduled workflows may be disabled automatically. When a public repository is forked, scheduled workflows are disabled by default. In a public repository, scheduled workflows are automatically disabled when no repository activity has occurred in 60 days.
>
> -- <a href="https://docs.github.com/en/actions/using-workflows/disabling-and-enabling-a-workflow"><cite>GitHub docs, Disabling and enabling a workflow</cite></a>

This action makes a scheduled workflow fail in order to warn the owner that the workflow is about to be disabled due to the above GitHub policy.

## How to use
### Quickstart
```yaml
name: CI

on:
  push:
    branches:
      - "**"
  pull_request:
    branches:
      - [YOUR MAIN BRANCH]
  schedule:
    - cron: "0 0 * * *"

jobs:
  test:
    runs-on: ubuntu-latest
    if: github.repository == '[YOUR ORGANIZATION]/[YOUR REPOSITORY]' && github.ref == 'refs/heads/[YOUR MAIN BRANCH]' && github.event_name == 'schedule'
    steps:
      - name: Warn if scheduled workflow is about to be disabled
        uses: fem-on-colab/warn-workflow-about-to-be-disabled-action@main
        with:
          workflow-filename: ci.yml
          main-branch: main
          days-elapsed: 55
          token: ${{ secrets.REPO_ACCESS_TOKEN }}
```
where `[YOUR ORGANIZATION]`, `[YOUR REPOSITORY]` and `[YOUR MAIN BRANCH]` are placeholders that have to be replaced with appropriate values.

### Options
| Option name | Description | Required | Default value |
|-------------|-------------|----------|---------------|
| `workflow-filename` | Filename of the workflow, without the leading `.github/workflows` prefix | `true` | (none) |
| `main-branch` | Name of the default branch | `false` | `main` |
| `days-elapsed` | Number of days elapsed from the previous repository activity to raise the warning | `true` | (none) |
| `token` | A fine-grained personal access token with at least read access to actions, code (= content), and metadata | `false` | `${{ github.token }}` |

## FAQ
1. *Who will receive the email notification?*\
   Notifications warning that the workflow is about to be disabled will be sent to the user who triggered the schedule. Their associated username can be easily looked up in any scheduled workflow run, below `Triggered via schedule`. The definition of the user who triggers the scheduled is as follows in the GitHub docs:
> Notifications for scheduled workflows are sent to the user who initially created the workflow. If a different user updates the cron syntax in the workflow file, subsequent notifications will be sent to that user instead. If a scheduled workflow is disabled and then re-enabled, notifications will be sent to the user who re-enabled the workflow rather than the user who last modified the cron syntax.
>
> -- <a href="https://docs.github.com/en/actions/using-workflows/disabling-and-enabling-a-workflow"><cite>GitHub docs, Notifications for workflow runs</cite></a>

2. *What will the workflow failure look like?*\
  The error message in the workflow failure contains the following text
> Workflow {workflow_filename} is going to be disabled in {number} days. To prevent this, please temporarily manually disable the workflow and then immediately re-enable it.

3. *How do I disable/enable a workflow?*\
   See [Disabling a workflow
](https://docs.github.com/en/actions/using-workflows/disabling-and-enabling-a-workflow#disabling-a-workflow) and [Enabling a workflow](https://docs.github.com/en/actions/using-workflows/disabling-and-enabling-a-workflow#enabling-a-workflow) on GitHub documentation.

4. *How is this action different from [Keepalive Workflow](https://github.com/marketplace/actions/keepalive-workflow)?*\
   The "Keepalive Workflow" action creates a dummy commit in the repository to keep the scheduled workflow alive.\
   One advantage of "Keepalive Workflow" is that, by creating a dummy commit, no intervention from the repository maintainer is required; this action, instead, does require manual intervention from the repository maintainer.\
   One disadvantage of "Keepalive Workflow" is that it pollutes the repository history on the main branch with dummy commits; this action, instead, does not add any commits to the repository.

5. *What value do you suggest for the `days-elapsed` option?*\
   The value should be less than 60, as the workflow is disabled after 60 days of activity. The value to use will depend on the periodicity of the scheduled run. For instance, for nightly scheduled runs we suggest to set `days-elapsed` to 55 in order to receive 5 notifications before the workflow is disabled.

6. *Why does this action require a `main-branch` option? Does the activity on another branch count as "repository activity"?*\
   GitHub only counts a commit on the main branch of the repository as "repository activity". Other actions, such as commits on another branch, do not count.

7. *Is the `token` option required for public repositories?*\
   The `token` option is typically only required for private repositories. See [Creating a fine-grained personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)  on GitHub documentation.

8. *Why is there a `if:` in the quickstart above?*\
   The condition `github.event_name == 'schedule'` is to ensure that this action does not get executed on runs that are not scheduled workflow runs.\
   The condition `github.repository == '[YOUR ORGANIZATION]/[YOUR REPOSITORY]'` is to avoid running this action on forks, as fork owners are typically not interested in running scheduled workflows.\
   The condition `github.ref == 'refs/heads/[YOUR MAIN BRANCH]'`, when listed alongside `github.event_name == 'schedule'`, is actually useless, but serves as a reminder that scheduled workflow runs only happen on the main branch of the repository.

9. *Does this action violate GitHub policies in terms of automatically disabling unused workflows?*\
   The web interface sometimes offers a "Continue running" button when scheduled workflows are approaching the 60 days deadline, but the availability of this button is not notified in any way to the repository maintainer. In the author's opinion, this action adheres to the spirit of the policy introduced by GitHub, in the sense that it merely provides an automated notification. Indeed, the repository maintainer still has to manually confirm their intention of keeping the scheduled workflow running, just as if they clicked on the "Continue running" button on the web page. In case of differing opinions, please contact [the author of this action](https://www.francescoballarin.it/).
