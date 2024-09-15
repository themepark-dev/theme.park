# Contributing to theme.park

- If you want to discuss changes, you can also bring it up in our Discord server
- PR's are done against the develop branch.

## Bug fixes

- When submitting bugfixes please show a before and after screenshot of the fix, and a description of what the fix does.

## New theme option

- The current variables in use can be found in any of the CSS files in `/css/theme-options/` and `/css/community-theme-options/`

- New community contributed theme options will be placed in the `Community Themes` category on our docs page.

- Community themes are not officially supported but as long as they follow the same variable structure as the other theme options it should look fine on all applications.

- When contributing a new option, you must have example screeenshots of the theme being used. Preferrably at least 10 with the same image size. See examples on our [docs page](https://docs.theme-park.dev/community-themes/).

### Specials

Remember to also to change the variables in the the `Specials` section even if you dont use the application the variable refers to.

- `--arr-queue-color` Please refrain from using an orange/yellowish color on the variable as its confusing from a UX standpoint as the "arrs" use that color range when something is wrong in the queue.

## New application theme

- When creating a new theme for an application please test multiple theme options to make sure it looks good on all options not just your favorite.

- The PR must contain a screenshot of all the different theme options. Optionally you can also include screenshots with the community theme options.
