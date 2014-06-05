# column 1: user_id
# column 2: review_count
# column 3: average_stars
# column 4: funny votes
# column 5: cool votes
# column 6: useful votes
# column 7: total votes
# column 8: percentage of funny votes
# column 9: percentage of cool votes
# column 10: percentage of useful votes

JSON=yelp_academic_dataset_user.json
TSV=yelp_academic_dataset_user.tsv

echo -n "# of users: "
wc -l $TSV 

echo "\ntop reviewers users are: "
sort -k2,2nr $TSV | head

echo "\nfunniest reviewers with at least 100 votes:"
perl -wlanF'\t' -E '$F[6] > 100 and say' $TSV | sort -k8,8nr | head

echo "\ninfrequent but useful reviewers:"
perl -wlanF'\t' -E '$F[1] < 25 and say' $TSV | sort -k7,7nr | head

echo "\nminimum # of reviews to show up in dataset is 1:"
sort -k2,2n $TSV | head

echo "\nextremely funny user's user ID"
perl -wlanF'\t' -E '$F[6] > 100 and ($F[7] > .9 || $F[8] > .9 || $F[9] > .9) and say' $TSV | sort -k8,8nr | head -1

ID=tZGbfA1WXE8bTsDmJXdO6w

echo "\nraw json entry for above"
grep tZGbfA1WXE8bTsDmJXdO6w $JSON
