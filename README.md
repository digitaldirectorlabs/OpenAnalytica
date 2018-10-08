**OpenAnalytica**
==============================
[GNU General Public License v3.0](https://github.com/digitaldirectorlabs/OpenAnalytica/blob/master/LICENSE)

OpenAnalytica is a Jupyter notebook with associated [Python (& Pandas)](https://pandas.pydata.org) scripts for taking a [free NationBuilder voter file](https://nationbuilder.com/voterfile) and generating voter demographic segments as CSVs for use in ad targeting on various social media platforms such as [Facebook](https://www.facebook.com/business/help/170456843145568), [YouTube](https://support.google.com/google-ads/answer/6379332?hl=en), and [Twitter](https://business.twitter.com/en/help/campaign-setup/campaign-targeting/tailored-audiences/TA-from-lists.html).

The tool provides:
* Data quality analysis and data cleaning of the voter file
* Data visualizations across various voter demographics and elections
* Segmented CSV files grouped by voter age, gender, and party affiliation
* Tutorial for using the newly generated CSV files for Facebook ad targeting

------------

# **Setup Instructions**
1) Set up your development environment with a new directory.  We recommend using [virtualenv](https://www.pythonforbeginners.com/basics/how-to-use-python-virtualenv).
2) Navigate to your new directory's bin folder and activate the virtualenv
```
cd /Users/MyUser/.virtualenvs/MyNewDirectory/bin
source activate
cd ..
```
3) Download or clone this repository into your new directory.
```git clone github_repository_url```
4) Install the requirements.txt file using
```pip install -r requirements.txt```
5) Move your NationBuilder voter file and voter history CSVs to the directory.
6) Open the Jupyter notebook from the terminal using ```ipython notebook``` , follow the file directory to the ```OpenAnalytica.ipynb``` file, and click to open it.  Please note, you will need to update the filepaths in the Jupyter notebook before starting.  Once that is complete use `SHIFT + ENTER`  to run the grey code cells.

------------

# **Tutorial**
Say an Independent candidate is running in a heavily Republican district.

First, the candidate must identify which age, gender, and party affiliation segments are most important to reach in order to secure 51% of the votes.  For example, by referencing our Jupyter notebook, we see in the last few elections voters aged 40 to 80 were most likely to vote...
![Output sample](https://github.com/digitaldirectorlabs/OpenAnalytica/gifs/DD_turnout_by_age.gif)

In the voter segments table, we can see that Republicans are the vast majority of voters in the district, along with a number of Swing voters and many Nonvoters...
![Output sample](https://github.com/digitaldirectorlabs/OpenAnalytica/gifs/DD_segments.gif)


Now say the candidate has a post about an important political issue.  The candidate's hypothesis is that the message will stick most with working age Female Swing voters. They can then test this hypothesis by targeting specifically those audiences on the social media platform of their choice. For example on [Facebook's Ad Manager](https://www.facebook.com/business/help/200000840044554), start by uploading the [custom audiences](https://www.facebook.com/business/a/custom-audiences) to target...
![Output sample](https://github.com/digitaldirectorlabs/OpenAnalytica/gifs/DD_voters_to_FB.gif)


Next, create a new Facebook ad campaign and in the adset's audience settings choose the newly created custom audiences you'd like to reach...
![Output sample](https://github.com/digitaldirectorlabs/OpenAnalytica/gifs/DD_target_voters.gif)


Looks like the candidate can reach between 640 and 2,000 female, working age, swing voters in the district with a targeted message!

Finally, the code generates a CSV of the voter segments table so you can keep track of each key segment you need to reach and their corresponding social media traction. That is - campaigns focused on measuring and growing metrics such as *likes, views, shares, subscriptions, and donations* for swayable, high turnout voter segments across multiple social media platforms such as *Facebook, YouTube, and Twitter* will have a great advantage on election day.


# **How To Contribute**
We hope others find this work useful, and encourage those wanting to collaborate to email us at *hello@digitaldirectorlabs.com*, sign up for our [email list](https://www.digitaldirectorlabs.com/contact) or fork the [repo](https://github.com/digitaldirectorlabs/OpenAnalytica).

# **Notes**
* NationBuilder voter files vary by size depending on the number of fields and the size of the voting district, ranging from 100 MB for a small state level campaign to 10 GB for a U.S. senate campaign.  A small voter file should take about 30 seconds to import while a larger voter file (up to 4 or 5GB total) will take up to an hour depending on the machine being used.
* [Facebook's new policies](https://www.facebook.com/business/m/one-sheeters/ads-with-political-content-us) for political advertising
* [Great resource](https://medium.com/political-moneyball/how-political-campaigns-are-wasting-thousands-of-dollars-on-facebook-93ec31535519) on how to spend advertising budget wisely on Facebook

