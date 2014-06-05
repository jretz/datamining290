#!/usr/bin/env perl
use v5.12.0;
use warnings FATAL => "all";
use autodie;
use Data::Dumper;
use JSON::XS;

my $users_input_file = "yelp_academic_dataset_user.json";
my $users_output_file = "yelp_academic_dataset_user.tsv";
open my $in, '<:crlf', $users_input_file;
open my $out, '>', $users_output_file;

while (defined(my $line = <$in>)){
    chomp $line;
    my $json = decode_json $line;
    my $total_votes = $json->{votes}{funny} + $json->{votes}{cool} + $json->{votes}{useful};
    say $out join("\t", 
        $json->{user_id},
        $json->{review_count},
        $json->{average_stars},
        $json->{votes}{funny},
        $json->{votes}{cool},
        $json->{votes}{useful},
        $total_votes,
        $total_votes > 0 ? (
            sprintf("%.2f", $json->{votes}{funny} / $total_votes),
            sprintf("%.2f", $json->{votes}{cool} / $total_votes),
            sprintf("%.2f", $json->{votes}{useful} / $total_votes),
        ): (0, 0, 0)
    );
}

close $out;
close $in;
