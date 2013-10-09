#!c:\Perl\bin\perl

# Prezentul simulator de examen impreuna cu formatul bazelor de intrebari, rezolvarile problemelor, manual de utilizare,
# instalare, SRS, cod sursa si utilitarele aferente constituie un pachet software gratuit care poate fi distribuit/modificat 
# in termenii licentei libere GNU GPL, asa cum este ea publicata de Free Software Foundation in versiunea 2 sau intr-o 
# versiune ulterioara. 
# Programul, intrebarile si raspunsurile sunt distribuite gratuit, in speranta ca vor fi folositoare, dar fara nicio garantie,
# sau garantie implicita, vezi textul licentei GNU GPL pentru mai multe detalii.
# Utilizatorul programului, manualelor, codului sursa si utilitarelor are toate drepturile descrise in licenta publica GPL.
# In distributia pe CD sau download pe www.yo6kxp.org trebuie sa gasiti o copie a licentei GNU GPL, de asemenea si versiunea 
# in limba romana, iar daca nu, ea poate fi descarcata gratuit de pe pagina http://www.fsf.org/
# Textul intebarilor oficiale publicate de ANRCTI face exceptie de la cele de mai sus, nefacand obiectul licentierii GNU GPL, 
# modificarea lor si/sau folosirea lor in afara Romaniei in alt mod decat read-only nefiind este permisa. Acest lucru deriva 
# din faptul ca ANRCTI este o institutie publica romana, iar intrebarile publicate au caracter de document oficial.
# Site-ul de unde se poate descarca distributia oficiala a simulatorului este http://www.yo6kxp.org

# This program together with question database formatting, solutions to problems, manuals, documentation, sourcecode and
# utilitiesis is a  free software; you can redistribute it and/or modify it under the terms of the GNU General Public License 
# as published by the Free Software Foundation; either version 2 of the License, or any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without any implied warranty. 
# See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this software distribution; if not, you can
# download it for free at http://www.fsf.org/ 
# Questions marked with ANRCTI makes an exception of above-written, as ANRCTI is a romanian public authority(similar to FCC in USA)
# so any use of the official questions, other than in Read-Only way, is prohibited. 

# YO6OWN Francisc TOTH, February 2010

#  sim_register.cgi v.3.0.3
#  Status: devel
#  This is a module of the online radioamateur examination program
#  "SimEx Radio", created for YO6KXP ham-club located in Sacele, ROMANIA
#  Made in Romania

# ch 3.0.3 inlocuit buton "window" cu form method="link"
# ch 3.0.2 - slash permitted again, for development purpose
# ch 3.0.1 eliminam / din caracterele ce pot forma login-ul
# ch 3.0.0 butonul de la OK face direct request de autentificare la authent.cgi(ad-hoc improvement idea)
# ch 0.0.7 fixed trouble ticket 26
# ch 0.0.6 forestgreen and aquamarine colors changed to hex value
# ch 0.0.5 W3C audit passed
# ch 0.0.4 solved trouble ticket nr.7
# ch 0.0.3 solved trouble ticket nr.1
# ch 0.0.2 solved trouble ticket nr. 4
# ch 0.0.1 generated from sim_register.cgi v.0.1.9, a HAM-eXam component

use strict;
use warnings;

sub ins_gpl;                 #inserts a HTML preformatted text with the GPL license text

#GLOBAL VARIABLES
#variables extracted from POST data
my $post_login;
my $post_passwd1;
my $post_passwd2;
my $post_tipcont;			#tip cont: 0-1,2,3,4

my $post_trid;

my $trid_login; #the username from the transactionfile, corresponding to the active transaction

#Global flags
my $f_valid_login;
my $f_valid_tipcont;
my $f_pass_eq;
my $f_xuser;					#flag says if login already exists in database

my @tridfile;					#slurped transaction file
my $trid;						#the Transaction-ID of the generated page

my @utc_time=gmtime(time);     	#the 'present' time, generated only once

my @slurp_userfile;            	#RAM-userfile

#BLOCK: Input: acquire input data
{
my $buffer;
my @pairs;
my $pair;
my $stdin_name;
my $stdin_value;


@pairs=split(/&/, $ENV{'QUERY_STRING'}); #GET-technology

foreach $pair(@pairs) {
($stdin_name,$stdin_value) = split(/=/,$pair);
$stdin_value=~ tr/+/ /;
$stdin_value=~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
$stdin_value=~ s/<*>*<*>//g;
if($stdin_name eq 'login') {$post_login=$stdin_value;}
elsif($stdin_name eq 'passwd1') {$post_passwd1=$stdin_value;}
elsif($stdin_name eq 'passwd2') {$post_passwd2=$stdin_value;}
elsif($stdin_name eq 'tipcont') {$post_tipcont=$stdin_value;}
elsif($stdin_name eq 'transaction') {$post_trid=$stdin_value;}
} #.end foreach
} #.end block
#.END BLOCK

#BLOCK: Refresh transaction file, rewrite but don't close file
{
#ACTION: open transaction ID file
open(transactionFILE,"+< sim_transaction") or die("can't open transaction file: $!\n");					#open transaction file for writing
#flock(transactionFILE,2);		#LOCK_EX the file from other CGI instances

#ACTION: refresh transaction file
seek(transactionFILE,0,0);		#go to the beginning
@tridfile = <transactionFILE>;		#slurp file into array

#$trid=$tridfile[0]; #debug
#chomp $trid;			#debug			#eliminate \n


my $act_sec=$utc_time[0];
my $act_min=$utc_time[1];
my $act_hour=$utc_time[2];
my $act_day=$utc_time[3];
my $act_month=$utc_time[4];
my $act_year=$utc_time[5];
my @livelist=();
my @linesplit;

unless($#tridfile == 0) 		#unless transaction list is empty (but transaction exists on first line)
{ #.begin unless
  for(my $i=1; $i<= $#tridfile; $i++)	#check all transactions 
  {
   @linesplit=split(/ /,$tridfile[$i]);
   chomp $linesplit[8]; #\n is deleted

if (($linesplit[2] > 3) && ($linesplit[2] < 8)) {@livelist=(@livelist, $i);}#if this is an exam transaction, don't touch it
# next 'if' is changed into 'elsif'
elsif($linesplit[8] > $act_year) {@livelist=(@livelist, $i);}  #it's alive one more year, keep it in the list
 elsif($linesplit[8] == $act_year){
 if($linesplit[7] > $act_month) {@livelist=(@livelist, $i);}  #it's alive one more month, keep it in the list
 elsif($linesplit[7] == $act_month){
 if($linesplit[6] > $act_day) {@livelist=(@livelist, $i);}  #it's alive one more day, keep it in the list
 elsif($linesplit[6] == $act_day){
 if($linesplit[5] > $act_hour) {@livelist=(@livelist, $i);}  #it's alive one more day, keep it in the list
 elsif($linesplit[5] == $act_hour){
 if($linesplit[4] > $act_min) {@livelist=(@livelist, $i);}  #it's alive one more day, keep it in the list
 elsif($linesplit[4] == $act_min){
 if($linesplit[3] > $act_sec) {@livelist=(@livelist, $i);}  #it's alive one more day, keep it in the list
 
 } #.end elsif min
 } #.end elsif hour
 } #.end elsif day
 } #.end elsif month
 } #.end elsif year
    
  } #.end for


my @extra=();
@extra=(@extra,$tridfile[0]);		#transactionID it's always alive

my $j;

foreach $j (@livelist) {@extra=(@extra,$tridfile[$j]);}
@tridfile=@extra;

} #.end unless

} #.END BLOCK

#BLOCK: extract data from actual transaction and then delete it
{
my @livelist=();
my @linesplit;
my $expired=1;  #flag which checks if transaction has expired

unless($#tridfile == 0) 		#unless transaction list is empty (but transaction exists on first line)
{  
  for(my $i=1; $i<= $#tridfile; $i++)	#check all transactions 
  {
   @linesplit=split(/ /,$tridfile[$i]);
   if($linesplit[0] eq $post_trid) {
   									$expired=0;
									$trid_login=$linesplit[1]; #extract trid_login
									#nu se adauga inregistrarea asta in @livelist
   									}
	else {@livelist=(@livelist, $i);} #se adauga celelalte inregistrari in livelist
  } #.end for

my @extra=();
@extra=(@extra,$tridfile[0]);		#transactionID it's always alive

my $j;

foreach $j (@livelist) {@extra=(@extra,$tridfile[$j]);}
@tridfile=@extra;
  
} #.end unless

if($expired) {
#Action: rewrite transaction file
truncate(transactionFILE,0);
seek(transactionFILE,0,0);				#go to beginning of transactionfile

for(my $i=0;$i <= $#tridfile;$i++)
{
printf transactionFILE "%s",$tridfile[$i]; #we have \n at the end of each element
}

close (transactionFILE) or die("cant close transaction file\n");

print qq!Content-type: text/html\n\n!;
print qq?<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">\n?; 
print qq!<html>\n!;
print qq!<head>\n<title>examen radioamator</title>\n</head>\n!;
print qq!<body bgcolor="#228b22" text="#7fffd4" link="white" alink="white" vlink="white">\n!;
ins_gpl();
print qq!v.3.0.3\n!; #version print for easy upload check
print qq!<br>\n!;
print qq!<h1 align="center">Formularul de examen a fost folosit deja sau a expirat</h1>\n!;
print qq!<form method="link" action="http://localhost/index.html">\n!;
print qq!<center><INPUT TYPE="submit" value="OK"></center>\n!;
print qq!</form>\n!; 
print qq!</body>\n</html>\n!;

exit();
				} #.end expired

} #.END BLOCK

#BLOCK: Verify the POST data
{
#Action: Verify validity of login if it's an append form
if($post_login =~ / /) { $f_valid_login=1; } #login has multiple words!
elsif($post_login =~ /\+/) { $f_valid_login=1; } #login has nasty character!
elsif($post_login =~ /%/) { $f_valid_login=1; } #login has nasty character!
elsif((length $post_login < 4) or (length $post_login > 25)) {$f_valid_login=1}
else { $f_valid_login=0;}

#Action: Verify passwords
if    ($post_passwd1 =~ / /){ $f_pass_eq=1; }  #if there are multiple words
elsif ($post_passwd2 =~ / /){ $f_pass_eq=1; }  #if there are multiple words
elsif ((length $post_passwd1 < 8) or (length $post_passwd1 > 25)) {$f_pass_eq=1;}
elsif ((length $post_passwd2 < 8) or (length $post_passwd2 > 25)) {$f_pass_eq=1;}
elsif ($post_passwd1 eq $post_passwd2) {$f_pass_eq=0;}
else {$f_pass_eq=1;}

#Action: Verify validity of tipcont. 0,1,2,3,4 only
if(($post_tipcont eq "0") || ($post_tipcont eq "1") || ($post_tipcont eq "2") || ($post_tipcont eq "3") || ($post_tipcont eq "4")) { $f_valid_tipcont=0;} #the condition is not accurate
else {$f_valid_tipcont=1;}
#$f_valid_tipcont=1;#debug only


$f_xuser=0;    #initializare


#ACTION: Verify for append only if login is unique in user database
#ACTION: open user account file

open(userFILE,"< sim_users") or die("can't open user file: $!\n");	#open user file for writing
#flock(userFILE,2);		#LOCK_EX the file from other CGI instances
seek(userFILE,0,0);		#go to the beginning
@slurp_userfile = <userFILE>;		#slurp file into array



#search record
unless($#slurp_userfile < 0) 		#unless  userlist is empty
{ #.begin unless
  for(my $account=0; $account < (($#slurp_userfile+1)/7); $account++)	#check userlist, account by account
  {
if($slurp_userfile[$account*7+0] eq "$post_login\n"){$f_xuser=1;}
  }
 } #.end unless empty userlist 

  
} #.END BLOCK

if($f_valid_login or $f_valid_tipcont or $f_pass_eq or $f_xuser)
#BLOCK: POST data is NOK, generate new form with a new transaction type 1/2
{
#Action: generate new transaction
$trid=$tridfile[0];
chomp $trid;						#eliminate \n

$trid=hex($trid);		#convert string to numeric

if($trid == 0xFFFFFF) {$tridfile[0] = sprintf("%+06X\n",0);}
else { $tridfile[0]=sprintf("%+06X\n",$trid+1);}                #cyclical increment 000000 to 0xFFFFFF
#ACTION: generate a new transaction for anonymous

#print qq!generate neww transaction<br>\n!;
my $exp_sec=$utc_time[0];
my $exp_min=$utc_time[1];
my $exp_hour=$utc_time[2];
my $exp_day=$utc_time[3];
my $exp_month=$utc_time[4];
my $exp_year=$utc_time[5];
my $carry1=0;
my $carry2=0;
my %month_days=(
    0 => 31,	#january
    1 => 28,	#february
    2 => 31,	#march
    3 => 30,	#april
    4 => 31,	#may
    5 => 30,    #june
    6 => 31,	#july
    7 => 31,	#august
    8 => 30,	#september
    9 => 31,	#october
   10 => 30, 	#november
   11 => 31     #december
);
my %month_bis_days=(
    0 => 31,	#january
    1 => 29,	#february, bisect
    2 => 31,	#march
    3 => 30,	#april
    4 => 31,	#may
    5 => 30,    #june
    6 => 31,	#july
    7 => 31,	#august
    8 => 30,	#september
    9 => 31,	#october
   10 => 30, 	#november
   11 => 31     #december
);


#CHANGE THIS for customizing
my $expire=15;		#15 minutes in this situation

#increment expiry time

#minute increment
$carry1= int(($exp_min+$expire)/60);		#check if minutes overflow
$exp_min=($exp_min+$expire)%60;			#increase minutes

#hour increment
$carry2= int(($exp_hour+$carry1)/24);		#check if hours overflow
$exp_hour=($exp_hour+$carry1)%24;		#increase hours

#day increment
if($exp_year%4) {
$carry1=int(($exp_day+$carry2)/($month_days{$exp_month}+1));  #check if day overflows
$exp_day=($exp_day+$carry2)%($month_days{$exp_month}+1); #increase day if so
	        }
else		{
$carry1=int(($exp_day+$carry2)/($month_bis_days{$exp_month}+1));  #check if day overflows
$exp_day=($exp_day+$carry2)%($month_bis_days{$exp_month}+1); #increase day if so
		}
if($carry1) {$exp_day=1;}	#day starts with 1-anomaly solution

#month increment
$carry2=int(($exp_month+$carry1)/12);
$exp_month=($exp_month+$carry1)%12;
#year increment
$exp_year += $carry2;

my $hexi=sprintf("%+06X",$trid);			#$trid e inca numar
my $entry;
$entry = "$hexi anonymous 1 $exp_sec $exp_min $exp_hour $exp_day $exp_month $exp_year\n";
#printf "new entry: $entry<br>\n";
@tridfile=(@tridfile,$entry); 				#se adauga tranzactia in array

#printf "new tridfile:<br> @tridfile[0..$#tridfile]<br>\n";
#Action: rewrite transaction file
truncate(transactionFILE,0);
seek(transactionFILE,0,0);				#go to beginning of transactionfile

#print "Tridfile length befor write: $#tridfile \n";
for(my $i=0;$i <= $#tridfile;$i++)
{
printf transactionFILE "%s",$tridfile[$i]; #we have \n at the end of each element
}

close (transactionFILE) or die("cant close transaction file\n");
#ACTION: Generate the form, again
print qq!Content-type: text/html\n\n!;
print qq?<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">\n?; 
print qq!<html>\n!;
print qq!<head>\n<title>examen radioamator</title>\n</head>\n!;
print qq!<body bgcolor="#228b22" text="#7fffd4" link="white" alink="white" vlink="white">\n!;
ins_gpl();
print qq!v.3.0.3\n!; #version print for easy upload check
print qq!<h1 align="center"><font color="yellow">Eroare de completare formular</font></h1>\n!;
print "<br>\n";
#Action: Error descriptions
#print qq!<font color="yellow">Erori:</font><br>\n!;
if($f_valid_login) {print qq!<font color="yellow">-nume utilizator formatat incorect(vezi mai jos)</font><br>\n!;}
if($f_xuser){print qq!<font color="yellow">-numele de utilizator ales exista deja. Alege-ti un alt login.</font><br>\n!;}
if($f_valid_tipcont) {print qq!<font color="red">-$post_tipcont nu este o valoare acceptata</font><br>\n!;} #should be written in cheat_log, but it's an anonymous
#if($f_xemail){print qq!<font color="yellow">-adresa de e-mail exista deja in baza noastra de date.</font><br>\n!;}
if($f_pass_eq){print qq!<font color="yellow">-cele doua parole nu sunt identice sau parola nu respecta normele de securitate(vezi mai jos)</font><br>\n!;}

print qq!<form action="http://localhost/cgi-bin/sim_register.cgi" method="get">\n!;
print qq!<center><b>Formular de inregistrare (valabil 15 minute)</b></center>\n!;

print qq!<table width="60%" align="center" border="1" cellpadding="4" cellspacing="2">\n!; 



print qq!<tr>\n!;
print qq!<td width="30%">!;
if($f_xuser or $f_valid_login) { print qq!<font color="yellow">Login:</font>!;}
else {print 'Login:';}
print qq!</td>\n!;

print qq!<td>!;
unless($f_xuser or $f_valid_login) {print qq!<input type="text" name="login"  value="$post_login" size="25">!;}
else {print qq!<input type="text" name="login" size="25">!;}
print qq!</td>\n!;
print qq!</tr>\n!;
	 
print qq!<tr>\n!;
print qq!<td width="30%">!;
if($f_pass_eq) { print qq!<font color="yellow">Parola:</font>!;}
else {print 'Parola:';}
print qq!</td>\n!;
print qq!<td>!;
if($f_pass_eq) {print qq!<input type="password" name="passwd1" size="25">!;}
else {print qq!<input type="password" name="passwd1" value="$post_passwd1" size="25">!;}
print qq!</td>\n!;
print qq!</tr>\n!;

print qq!<tr>\n!;
print qq!<td width="30%">!;
if($f_pass_eq) { print qq!<font color="yellow">Parola, din nou:</font>!;}
else {print 'Parola, din nou:';}
print qq!</td>\n!;
print qq!<td>!;
if($f_pass_eq) {print qq!<input type="password" name="passwd2" size="25">!;}
else {print qq!<input type="password" name="passwd2" value="$post_passwd2" size="25">!;}
print qq!</td>\n!;
print qq!</tr>\n!;

print qq!<tr>\n!;
print qq!<td width="30%">Tipul contului:</td>\n!;
print qq!<td><select size="1" name="tipcont">\n!;

print qq!<option value="0" !;
if(!$f_valid_tipcont && $post_tipcont eq "0"){ print qq!selected="y" !;}
print qq!>Cont de antrenament</option>\n!;

print qq!<option value="1" !;
if(!$f_valid_tipcont && ($post_tipcont eq "1")){ print qq!selected="y" !;}
print qq!>Examen simulat clasa I</option>\n!;

print qq!<option value="2" !;
if(!$f_valid_tipcont && ($post_tipcont eq "2")){ print qq!selected="y" !;}
print qq!>Examen simulat clasa II</option>\n!;

print qq!<option value="3" !;
if(!$f_valid_tipcont && ($post_tipcont eq "3")){ print qq!selected="y" !;}
print qq!>Examen simulat clasa III</option>\n!;

print qq!<option value="4" !;
if(!$f_valid_tipcont && ($post_tipcont eq "4")){ print qq!selected="y" !;}
print qq!>Examen simulat clasa III-R</option>\n!;

print qq!</select>\n!;
print qq!</td>\n!;
print qq!</tr>\n!;




print qq!<tr>\n!;
print qq!<td width="33%">!;
print qq!<center><INPUT type="submit"  value="Inregistreaza"> </center>!;
print qq!</td>\n!;

print qq!<td>!;
print qq!<center><INPUT type="reset"  value="Reset"> </center>!;
print qq!</td>\n!;

print qq!</tr>\n!;

print qq!</table>\n!;



#ACTION: inserare transaction ID in pagina HTML
{
my $extra=sprintf("%+06X",$trid);
print qq!<input type="hidden" name="transaction" value="$extra">\n!;
}

print qq!</form>\n!;

print qq!<form method="link" action="http://localhost/index.html">\n!;
print qq!<center><INPUT TYPE="submit" value="Abandon Inregistrare"></center>\n!; 
print qq!</form>\n!; 

print qq!<p>\n!;
print qq!Login trebuie sa aiba intre 4 si 25 caractere. Nu se accepta caractere speciale: %, space; login-ul trebuie sa fie unic si sa nu fie folosit deja. <br>\n!;
print qq!Parola si noua introducere a parolei trebuie sa aiba intre 8 si 25 caractere; trebuie sa fie congruente; nu pot contine caracterele %, space;<br>\n!; 

print qq!</body>\n</html>\n!;
#ACTION: exit this process since it was an error
exit(); #ACTIVATE THIS since I think it must be here
} #.END BLOCK (NOK)
else
#BLOCK: POST data is OK, write it in userfile
{

#Action: rewrite transaction file
truncate(transactionFILE,0);
seek(transactionFILE,0,0);				#go to beginning of transactionfile

for(my $i=0;$i <= $#tridfile;$i++)
{
printf transactionFILE "%s",$tridfile[$i]; #we have \n at the end of each element
}

close (transactionFILE) or die("cant close transaction file\n");

#BLOCK: re/write new user record
{
my $new_expiry; #generat

#ACTION: open user account file
open(userFILE,"+< sim_users") or die("can't open user file: $!\n");	#open user file for writing
#flock(userFILE,2);		#LOCK_EX the file from other CGI instances
seek(userFILE,0,0);		#go to the beginning
@slurp_userfile = <userFILE>;		#slurp file into array

#ACTION: generate account expiry time = +7 days from now
my $exp_sec=$utc_time[0];
my $exp_min=$utc_time[1];
my $exp_hour=$utc_time[2];
my $exp_day=$utc_time[3];
my $exp_month=$utc_time[4];
my $exp_year=$utc_time[5];
my $carry1=0;
my $carry2=0;
my %month_days=(
    0 => 31,	#january
    1 => 28,	#february
    2 => 31,	#march
    3 => 30,	#april
    4 => 31,	#may
    5 => 30,    #june
    6 => 31,	#july
    7 => 31,	#august
    8 => 30,	#september
    9 => 31,	#october
   10 => 30, 	#november
   11 => 31     #december
);
my %month_bis_days=(
    0 => 31,	#january
    1 => 29,	#february, bisect
    2 => 31,	#march
    3 => 30,	#april
    4 => 31,	#may
    5 => 30,    #june
    6 => 31,	#july
    7 => 31,	#august
    8 => 30,	#september
    9 => 31,	#october
   10 => 30, 	#november
   11 => 31     #december
);

#CHANGE THIS if you want to customize
#$carry1=1; #1 month from now until the account expires

#CHANGE THIS if you want to customize
$carry2=7;  #account lives 7 days


#day increment
if($exp_year%4) {
$carry1=int(($exp_day+$carry2)/($month_days{$exp_month}+1));  #check if day overflows
$exp_day=($exp_day+$carry2)%($month_days{$exp_month}+1); #increase day if so
	        }
else		{
$carry1=int(($exp_day+$carry2)/($month_bis_days{$exp_month}+1));  #check if day overflows
$exp_day=($exp_day+$carry2)%($month_bis_days{$exp_month}+1); #increase day if so
		}
if($carry1) {$exp_day=1;}	#day starts with 1-anomaly solution

#month increment
$carry2=int(($exp_month+$carry1)/12);
$exp_month=($exp_month+$carry1)%12;
#year increment
$exp_year += $carry2;

$new_expiry = "$exp_sec $exp_min $exp_hour $exp_day $exp_month $exp_year\n"; #\n is important

#ACTION: Append new record
@slurp_userfile = (@slurp_userfile,"$post_login\n"); #add login
@slurp_userfile = (@slurp_userfile,"0 0 0 0 0 0\n"); #add next allowed login time
@slurp_userfile = (@slurp_userfile,"$post_passwd1\n"); #add password
@slurp_userfile = (@slurp_userfile,"0\n"); #add unsuccessful login attempts
@slurp_userfile = (@slurp_userfile,$new_expiry); #add account expiry time
@slurp_userfile = (@slurp_userfile,"$post_tipcont\n"); #add tip cont
@slurp_userfile = (@slurp_userfile,"0\n"); #add ultima clasa obtinuta

#ACTION: hard-rewrite userfile
truncate(userFILE,0);			#
seek(userFILE,0,0);				#go to beginning of transactionfile
for(my $i=0;$i <= $#slurp_userfile;$i++)
{
printf userFILE "%s",$slurp_userfile[$i]; #we have \n at the end of each element
}

close(userFILE);
} #.end BLOCK: re/write new user record


print qq!Content-type: text/html\n\n!;
print qq?<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">\n?; 
print qq!<html>\n!;
print qq!<head>\n<title>examen radioamator</title>\n</head>\n!;
print qq!<body bgcolor="#228b22" text="#7fffd4" link="white" alink="white" vlink="white">\n!;
ins_gpl();
print qq!v.3.0.3\n!; #version print for easy upload check
print qq!<h1 align="center">Inregistrare reusita.</h1>\n!;
print "<br>\n";

print "<center>Acum puteti sa va autentificati cu noile date.</center>\n";
print qq!<center>\n!;
print qq!<form action="http://localhost/cgi-bin/sim_authent.cgi" method="get">\n!;
print qq!<input type="hidden" name="login"  value="$post_login">!;
print qq!<input type="hidden" name="passwd" value="$post_passwd1">!;
print qq!<center><INPUT type="submit"  value="OK"> </center>!;
print qq!</form>\n!; 
print qq!</center>\n!;
print "</body>\n</html>\n";

} #.END BLOCK (OK)
#--------------------------------------
sub ins_gpl
{
print qq+<!--\n+;
print qq!SimEx Radio Release \n!;
print qq!SimEx Radio was created for YO6KXP ham-club located in Sacele, ROMANIA\n!;
print qq!\n!;
print qq!Prezentul simulator de examen impreuna cu formatul bazelor de intrebari, rezolvarile problemelor, manual de utilizare,!;
print qq!instalare, SRS, cod sursa si utilitarele aferente constituie un pachet software gratuit care poate fi distribuit/modificat!; 
print qq!in termenii licentei libere GNU GPL, asa cum este ea publicata de Free Software Foundation in versiunea 2 sau intr-o !;
print qq!versiune ulterioara.\n!; 
print qq!Programul, intrebarile si raspunsurile sunt distribuite gratuit, in speranta ca vor fi folositoare, dar fara nicio garantie,!;
print qq!sau garantie implicita, vezi textul licentei GNU GPL pentru mai multe detalii.\n!;
print qq!Utilizatorul programului, manualelor, codului sursa si utilitarelor are toate drepturile descrise in licenta publica GPL.\n!;
print qq!In distributia pe CD sau download pe www.yo6kxp.org trebuie sa gasiti o copie a licentei GNU GPL, de asemenea si versiunea !;
print qq!in limba romana, iar daca nu, ea poate fi descarcata gratuit de pe pagina http://www.fsf.org/\n!;
print qq!Textul intebarilor oficiale publicate de ANRCTI face exceptie de la cele de mai sus, nefacand obiectul licentierii GNU GPL,!; 
print qq!modificarea lor si/sau folosirea lor in afara Romaniei in alt mod decat read-only nefiind este permisa. Acest lucru deriva !;
print qq!din faptul ca ANRCTI este o institutie publica romana, iar intrebarile publicate au caracter de document oficial.\n!;
print qq!Site-ul de unde se poate descarca distributia oficiala a simulatorului este http://www.yo6kxp.org\n!;
print qq!YO6OWN Francisc TOTH\n!;
print qq!\n!;
print qq!This program together with question database formatting, solutions to problems, manuals, documentation, sourcecode and!;
print qq!utilitiesis is a  free software; you can redistribute it and/or modify it under the terms of the GNU General Public License !;
print qq!as published by the Free Software Foundation; either version 2 of the License, or any later version.\n!;
print qq!This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without any implied warranty.!; 
print qq!See the GNU General Public License for more details.\n!;
print qq!You should have received a copy of the GNU General Public License along with this software distribution; if not, you can!;
print qq!download it for free at http://www.fsf.org/\n!; 
print qq!Questions marked with ANRCTI makes an exception of above-written, as ANRCTI is a romanian public authority(similar to FCC in USA)!;
print qq!so any use of the official questions, other than in Read-Only way, is prohibited.\n!; 
print qq!YO6OWN Francisc TOTH, 2008\n!;
print qq!\n!;

print qq!Made in Romania\n!;
print qq+-->\n+;

}