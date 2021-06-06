# login info
login_area = '//div[contains(@class, "hm-MainHeaderRHSLoggedOutWide_Login")]'
login_username = '//input[contains(@class, "lms-StandardLogin_Username")]'
login_password = '//input[contains(@class, "lms-StandardLogin_Password")]'
login_btn = '//div[contains(@class, "lms-StandardLogin_LoginButton")]'

# top button
sports_btn = '//div[contains(@class, "hm-MainHeaderCentreWide_Link")]/div[contains(text(), "Sports")]'
in_play_btn = '//div[contains(@class, "hm-MainHeaderCentreWide_Link")]/div[contains(text(), "In-Play")]'
my_bets_btn = '//div[contains(@class, "hm-MainHeaderCentreWide_Link")]/div[contains(text(), "My Bets")]'

# in-play >
soccer_icon = '//div[contains(@class, "cil-ClassificationIconLarge-1")]'
top_game = '//div[contains(@class, "ovm-CompetitionList")]/div[1]/div[contains(@class, "ovm-FixtureList")]/div[1]/div/div[contains(@class, "ovm-FixtureDetailsTwoWay")]'
closed_league = '//div[contains(@class, "ipn-Competition-closed")]'

# game lavel
lavel_play_time = '//div[contains(@class, "ipn-Fixture_TimerContainer")]'
team_name_1 = '//div[contains(@class, "ipn-Fixture_TeamStack")]/div[1]'
team_name_2 = '//div[contains(@class, "ipn-Fixture_TeamStack")]/div[2]'
lavel_score_1 = '//div[contains(@class, "ipn-ScoresDefault_Score")]/div[1]'
lavel_score_2 = '//div[contains(@class, "ipn-ScoresDefault_Score")]/div[2]'

# soccer game bet type
amg = '//div[contains(text(), "Alternative Match Goals")]'
all_amg_under = '//div[contains(text(), "Alternative Match Goals")]/parent::node()/following-sibling::div[1]/div/div/div[contains(@class, "srb-ParticipantLabelCentered")]'

# stats info
stats = '//div[contains(@class, "ml-StatButtons_Button-stats")]'
attacks_1 = '//div[contains(text(), "Attacks") and not(contains(text(), "Dangerous Attacks"))]/following-sibling::div[1]/div[1]'
attacks_2 = '//div[contains(text(), "Attacks") and not(contains(text(), "Dangerous Attacks"))]/following-sibling::div[1]/div[3]'
d_attacks_1 = '//div[contains(text(), "Dangerous Attacks")]/following-sibling::div[1]/div[1]'
d_attacks_2 = '//div[contains(text(), "Dangerous Attacks")]/following-sibling::div[1]/div[3]'
possession_1 = '//div[contains(text(), "Possession %")]/following-sibling::div[1]/div[1]'
possession_2 = '//div[contains(text(), "Possession %")]/following-sibling::div[1]/div[3]'
yellow_card_1 = '//div[contains(@class, "ml1-StatsLower")]/div[1]/div/div/div[1]/div[2]'
yellow_card_2 = '//div[contains(@class, "ml1-StatsLower")]/div[3]/div/div/div[3]/div[2]'
red_card_1 = '//div[contains(@class, "ml1-StatsLower")]/div[1]/div/div/div[2]/div[2]'
red_card_2 = '//div[contains(@class, "ml1-StatsLower")]/div[3]/div/div/div[2]/div[2]'
corner_kick_1 = '//div[contains(@class, "ml1-StatsLower")]/div[1]/div/div/div[3]/div[2]'
corner_kick_2 = '//div[contains(@class, "ml1-StatsLower")]/div[3]/div/div/div[1]/div[2]'
on_target_1 = '//div[contains(@class, "ml1-StatsLower_MiniBarsCollection")]/div[1]/div/div/b[1]'
on_target_2 = '//div[contains(@class, "ml1-StatsLower_MiniBarsCollection")]/div[1]/div/div/b[2]'
off_target_1 = '//div[contains(@class, "ml1-StatsLower_MiniBarsCollection")]/div[2]/div/div/b[1]'
off_target_2 = '//div[contains(@class, "ml1-StatsLower_MiniBarsCollection")]/div[2]/div/div/b[2]'

# summary info
summary = '//div[contains(@class, "ml-StatButtons_Button-summary")]'
show_more = '//div[contains(@class, "ml-Summary_Link")]'
play_time = '//time[contains(@class, "ml-Timeline_Time")]'
shifts_1 = '//div[contains(@class, "ml1-StatBoardColumn_Icon-9")]/following-sibling::div[1]'
shifts_2 = '//div[contains(@class, "ml1-StatBoardColumn_Icon-9")]/following-sibling::div[2]'
pk_1 = '//div[contains(@class, "ml1-StatBoardColumn_Icon-8")]/following-sibling::div[1]'
pk_2 = '//div[contains(@class, "ml1-StatBoardColumn_Icon-8")]/following-sibling::div[2]'
goal_1 = '//div[contains(@class, "ml1-StatBoardColumn_Icon-1")]/following-sibling::div[1]'
goal_2 = '//div[contains(@class, "ml1-StatBoardColumn_Icon-1")]/following-sibling::div[2]'
home_goals = '//div[contains(@class, "ml-SummaryRow_TextIcon-1")]/span[contains(@class, "ml1-SoccerSummaryRow_GoalText")]/../following-sibling::div[1]'
away_goals = '//div[contains(@class, "ml-SummaryRow_TextIcon-2")]/span[contains(@class, "ml1-SoccerSummaryRow_GoalText")]/../preceding-sibling::div[1]'
