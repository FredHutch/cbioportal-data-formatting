#! usr/bin/env perl
use strict;
use warnings FATAL => 'all';
use Try::Tiny;

my $in=shift;
my $in2=shift;
my %hash;
my %cbio;

open IN, $in;
while(<IN>){
	chomp;
	my @a=split(/\t/,$_);
	if (@a == 2){
		$hash{$a[0]}=$a[1];
	}
	# Some genes have no Entrez ID, set to 0
	else{
		$hash{$a[0]} = 0;
	}
}
open IN2, $in2;
while(<IN2>){
	try{
		chomp;
		my @b=split(/\t/,$_);
		my $num=$b[3];
		if (exists $hash{$b[-1]}){
			my $as="$b[-1]\t$hash{$b[-1]}";
	#			print "$b[-1]\t$hash{$b[-1]}\t$num\n";
				$cbio{$as}=$num;
				}
		}
		catch{
			warn "error thrown: $_ for file $in2\n";
			die;
		}
	}
foreach my $key (sort keys %cbio){
	print "$key\t$cbio{$key}\n";
		}
