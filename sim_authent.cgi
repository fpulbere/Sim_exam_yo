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
# Textul intebarilor oficiale publicate de ANCOM face exceptie de la cele de mai sus, nefacand obiectul licentierii GNU GPL, 
# modificarea lor si/sau folosirea lor in afara Romaniei in alt mod decat read-only nefiind este permisa. Acest lucru deriva 
# din faptul ca ANCOM este o institutie publica romana, iar intrebarile publicate au caracter de document oficial.
# Site-ul de unde se poate descarca distributia oficiala a simulatorului este http://www.yo6kxp.org

# This program together with question database formatting, solutions to problems, manuals, documentation, sourcecode and
# utilitiesis is a  free software; you can redistribute it and/or modify it under the terms of the GNU General Public License 
# as published by the Free Software Foundation; either version 2 of the License, or any later version.
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without any implied warranty. 
# See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this software distribution; if not, you can
# download it for free at http://www.fsf.org/ 
# Questions marked with ANCOM makes an exception of above-written, as ANCOM is a romanian public authority(similar to FCC in USA)
# so any use of the official questions, other than in Read-Only way, is prohibited. 

# (c) YO6OWN Francisc TOTH, 2008 - 2013

#  sim_authent.cgi v.3.0.f 
#  Status: devel
#  This is a module of the online radioamateur examination program
#  "SimEx Radio", created for YO6KXP ham-club located in Sacele, ROMANIA
#  Made in Romania


# ch 3.0.f inlocuit window-button cu method="link" button
# ch 3.0.e am explicat la legenda acoperirea cu intrebari
# ch 3.0.d @slash@ replaces / corect, acum
# ch 3.0.c @slash@ replaces /
# ch 3.0.b radio butonul nu se mai afiseaza deloc
# ch 3.0.a rezolvat tichetul cu astfel, astfel, astfel
# ch 3.0.9 nu se vede diferit checkbox=off fata de on, cel off schimbat cu buton radio disable
# ch 3.0.8 functionalitatea secreta denumita Lupa Convergenta(TM)
# ch 3.0.7 corrected custom bug
# ch 3.0.6 explicatii pentru super-incepatori
# ch 3.0.5 evidentiat subcapitolele cu erori
# ch 3.0.4 merge pentru clasele 1-4
# ch 3.0.3 la fiecare sf. de capitol de programa link UP la o ancora #begin.
# ch 3.0.2 afisarea programei, cu "acoperiri", customizat pt clasa 1 doar
# ch 3.0.1 avem o afisare a programei(din 4 sau 3 bucati, dupa clasa)
# ch 3.0.0 se sterge fisierul tip hlr cand userul expira
# ch 0.0.9 fixed trouble ticket 26
# ch 0.0.8 fixed trouble ticket 28
# ch 0.0.7 fixed trouble ticket 9
# ch 0.0.6 forestgreen and aquamarine were changed to hex values
# ch 0.0.5 W3C audit passed
# ch 0.0.4 specificat cine este examinatorul = cel care a creat contul
# ch 0.0.3 fixed trouble ticket 2
# ch 0.0.2 fixed trouble ticket 3 
# ch 0.0.1 generated from authent.cgi vers 0.1.10 

use strict;
use warnings;

sub punishment($);           #where user gets kicked for abandoned exams
sub ins_gpl;                 #inserts a HTML preformatted text with the GPL license text

my $get_login;                 	#submitted login
my $get_passwd;                	#submitted password

my @slurp_userfile;            	#RAM-userfile
my @utc_time=gmtime(time);     	#the 'present' time, generated only once

my $rec_pos=-1;			#user record position, init is 'not found'

my @tridfile;			#slurped transaction file
my $trid;			#the Transaction-ID of the generated page

my $hlr_filename; #numele fisierului hlr (V3 stuff)
my $hlrclass;	  #stringul "clasa1" "clasa2" "clasa3" "clasa4"
my @materii;	  #sirul cu materii-programa
my @strips;	  #contains list with files containing only v3-codes
my @slurp_strip;  #slurped content of such a file

my $fileline;	  #fetches line by line

my %hlrline;
my @splitter;
my $found;

#BLOCK: Input:login string-user+password
{
my $buffer;
my @pairs;
my $pair;
my $stdin_name;
my $stdin_value;

@pairs=split(/&/, $ENV{'QUERY_STRING'}); #GET-technology

#verificare ca sa existe exact 2 perechi: login si passwd
unless($#pairs == 1) #exact 2 perechi: p0 si p1
{
#ACTION: append cheat symptoms in cheat file
open(cheatFILE,"+< cheat_log") or die("can't open cheat_log file: $!\n");					#open transaction file for writing
#flock(cheatFILE,2);		#LOCK_EX the file from other CGI instances

#ACTION: write in logfile
seek(cheatFILE,0,2);		#go to the end
#CUSTOM
printf cheatFILE "sim_authent.cgi:instead of 2 pairs, %i pair(s) received. Received: [%s]\n",$#pairs+1,$ENV{'QUERY_STRING'};
close(cheatFILE);

#ACTION: display a defeat page
print qq!Content-type: text/html\n\n!;
print qq?<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">\n?; 
print qq!<html>\n!;
print qq!<head>\n<title>examen radioamator</title>\n</head>\n!;
print qq!<body bgcolor="#228b22" text="#7fffd4" link="white" alink="white" vlink="white">\n!;
ins_gpl();
print qq!v.3.0.f\n!; #version print for easy upload check
#print qq![$debug_buffer]\n!; #debug
print qq!<br>\n!;
print qq!<h1 align="center">Date corupte, situatie inregistrata in log.</h1>\n!;
print qq!<h2 align="center">In cazul in care considerati ca acest mesaj nu ar fi trebuit sa apara, fiindca ati
 respectat pasii corecti, va rog sa-mi trimiteti pe e-mail o descriere cat mai exacta a 
actiunilor care au dus la aparitia acestei pagini de eroare, pentru investigare. TNX de YO6OWN</h2>\n!;
print qq!<form method="link" action="http://localhost/index.html">\n!;
print qq!<center><INPUT TYPE="submit" value="OK"></center>\n!;
print qq!</form>\n!; 
print qq!</body>\n</html>\n!;

#ACTION: exit page since an error was detected
exit();
}
#end number consistency check

foreach $pair(@pairs) {
($stdin_name,$stdin_value) = split(/=/,$pair);
$stdin_value=~ tr/+/ /;
$stdin_value=~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
$stdin_value=~ s/<*>*<*>//g;

if($stdin_name eq 'login') { $get_login=$stdin_value;}
elsif($stdin_name eq 'passwd'){$get_passwd=$stdin_value;}

#daca nu au fost cum trebuie, cel putin una din ele a ramas undefined
#patch: consistency check, not tested

unless((defined $get_login) or (defined $get_passwd))
{
#ACTION: append cheat symptoms in cheat file
open(cheatFILE,"+< cheat_log") or die("can't open cheat_log file: $!\n");					#open transaction file for writing
#flock(cheatFILE,2);		#LOCK_EX the file from other CGI instances

#ACTION: write in logfile
seek(cheatFILE,0,2);		#go to the end
#CUSTOM
print cheatFILE "sim_authent.cgi: one of login&password remained undefined\n";
close(cheatFILE);

#ACTION: display a defeat page
print qq!Content-type: text/html\n\n!;
print qq?<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">\n?; 
print qq!<html>\n!;
print qq!<head>\n<title>examen radioamator</title>\n</head>\n!;
print qq!<body bgcolor="#228b22" text="#7fffd4" link="white" alink="white" vlink="white">\n!;
ins_gpl();
print qq!v.3.0.f\n!; #version print for easy upload check
#print qq![$debug_buffer]\n!; #debug
print qq!<br>\n!;
print qq!<h1 align="center">Date corupte, situatie inregistrata in log.</h1>\n!;
print qq!<h2 align="center">In cazul in care considerati ca acest mesaj nu ar fi trebuit sa apara, fiindca ati
 respectat pasii corecti, va rog sa-mi trimiteti pe e-mail o descriere cat mai exacta a 
actiunilor care au dus la aparitia acestei pagini de eroare, pentru investigare. TNX de YO6OWN</h2>\n!;
print qq!<form method="link" action="http://localhost/index.html">\n!;
print qq!<center><INPUT TYPE="submit" value="OK"></center>\n!;
print qq!</form>\n!; 
print qq!</body>\n</html>\n!;

#ACTION: exit page since an error was detected
exit();
}
 

} #.end foreach
} #.end block
#.END BLOCK

#BLOCK: open userfile; Refresh userfile with criteria expiry time.
{
#ACTION: open user account file
open(userFILE,"+< sim_users") or die("can't open user file: $!\n");					#open user file for writing
#flock(userFILE,2);		#LOCK_EX the file from other CGI instances

#ACTION: refresh user accounts, delete expired accounts
seek(userFILE,0,0);		#go to the beginning
@slurp_userfile = <userFILE>;		#slurp file into array

my $act_sec=$utc_time[0];
my $act_min=$utc_time[1];
my $act_hour=$utc_time[2];
my $act_day=$utc_time[3];
my $act_month=$utc_time[4];
my $act_year=$utc_time[5];

my @livelist=();
my @linesplit;

unless($#slurp_userfile < 0) 		#unless  userlist is empty
{ #.begin unless
  for(my $account=0; $account < (($#slurp_userfile+1)/7); $account++)	#check userlist, account by account
  {
   @linesplit=split(/ /,$slurp_userfile[$account*7+4]); #extract time line
#===========V3==============================
# aici trebuie extras numele userilor pe rand pentru faza de unlink hlr files pentru expirati 
 $hlr_filename=$slurp_userfile[$account*7+0];
 chomp $hlr_filename;
 $hlr_filename =~ s/\//\@slash\@/; # spec char / is replaced
#===========================================
   chomp $linesplit[5];		#otherwise $linesplit[5]='ab\n'
    
if($linesplit[5] > $act_year) {@livelist=(@livelist, $account);}  #it's alive one more year, keep it in the list
elsif($linesplit[5] == $act_year){
if($linesplit[4] > $act_month) {@livelist=(@livelist, $account);}  #it's alive one more month, keep it in the list
elsif($linesplit[4] == $act_month){
if($linesplit[3] > $act_day) {@livelist=(@livelist, $account);}  #it's alive one more day, keep it in the list
elsif($linesplit[3] == $act_day){
if($linesplit[2] > $act_hour) {@livelist=(@livelist, $account);}  #it's alive one more hour, keep it in the list
elsif($linesplit[2] == $act_hour){
if($linesplit[1] > $act_min) {@livelist=(@livelist, $account);}  #it's alive one more minute, keep it in the list
elsif($linesplit[1] == $act_min){
if($linesplit[0] > $act_sec) {@livelist=(@livelist, $account);}  #it's alive one more second, keep it in the list
else {if(-e "hlr/$hlr_filename") {unlink("hlr/$hlr_filename");}} #V3 mod

 } #.end elsif min
else {if(-e "hlr/$hlr_filename") {unlink("hlr/$hlr_filename");}}#V3 mod

 } #.end elsif hour
else {if(-e "hlr/$hlr_filename") {unlink("hlr/$hlr_filename");}}#V3 mod

 } #.end elsif day
else {if(-e "hlr/$hlr_filename") {unlink("hlr/$hlr_filename");}}#V3 mod

 } #.end elsif month
else {if(-e "hlr/$hlr_filename") {unlink("hlr/$hlr_filename");}}#V3 mod

 } #.end elsif year
else {if(-e "hlr/$hlr_filename") {unlink("hlr/$hlr_filename");}}#V3 mod
   
  } #.end for

#===========V3==============================
# un else {} general 'it's not alive' - aici se face unlink(); 
# functioneaza, dar trebuie verificata corectitudinea pentru toate cazurile
#===========================================

##we have now the list of the live user accounts
#print "@livelist[0..$#livelist]\n";   #debug only
my @extra=();
my $accnt;
foreach $accnt (@livelist) 
        {@extra=(@extra,$slurp_userfile[$accnt*7],
		        $slurp_userfile[$accnt*7+1],
						$slurp_userfile[$accnt*7+2],
						$slurp_userfile[$accnt*7+3],
						$slurp_userfile[$accnt*7+4],
						$slurp_userfile[$accnt*7+5],
						$slurp_userfile[$accnt*7+6]
					#	$slurp_userfile[$accnt*11+7],
					#	$slurp_userfile[$accnt*11+8],
					#	$slurp_userfile[$accnt*11+9],
					#	$slurp_userfile[$accnt*11+10],
                 );
         }
#print "@extra[0..10]\n";
@slurp_userfile=@extra;
#@extra=(); #obsolete

#ACTION: re-write the userdata file
truncate(userFILE,0);			#
seek(userFILE,0,0);				#go to beginning of transactionfile
for(my $i=0;$i <= $#slurp_userfile;$i++)
{
printf userFILE "%s",$slurp_userfile[$i]; #we have \n at the end of each element
}


} #.end unless
else #the case when user database is empty
{
print qq!Content-type: text/html\n\n!;
print qq?<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">\n?; 
print qq!<html>\n!;
print qq!<head>\n<title>examen radioamator</title>\n</head>\n!;
print qq!<body bgcolor="#228b22" text="#7fffd4" link="white" alink="white" vlink="white">\n!;
ins_gpl();
print qq!v.3.0.f\n!; #version print for easy upload check
#print qq![$debug_buffer]\n!; #debug
print qq!<br>\n!;
print qq!<br>\n!;
print qq!<h3 align="center">Numele dumneavoastra de utilizator nu se gaseste in baza noastra de date.</h3> <br>\n!;
print qq!<h3 align="center">ATENTIE: Daca ati avut cont si nu mai sunteti in baza de date, inseamna ca nu v-ati mai logat de peste 7 zile, contul se sterge automat. Va rugam consultati manualul.</h3>\n!;
print qq!<form method="link" action="http://localhost/index.html">\n!;
print qq!<center><INPUT TYPE="submit" value="OK"></center>\n!;
print qq!</form>\n!; 
print qq!</body>\n</html>\n!;

close(userFILE) or die("cant close user file\n"); 
exit(); #user database empty, no reason to continue. Exit after ERR page
}

} #.end block
#.END BLOCK

#BLOCK: $get_login found in userfile?
{
my $account;
my @linesplit;



  for(my $account=0; $account < (($#slurp_userfile+1)/7); $account++)	#check userlist, account by account
  {
   @linesplit=split(/\n/,$slurp_userfile[$account*7+0]); #linesplit[1] is \n, don't care

   if($linesplit[0] eq $get_login) {
					$rec_pos=$account;					#mark the good record
					$account=($#slurp_userfile+1)/7; 	#finish search
				    }

  } #.end for

#if login was not found, print error page, close resources and exit
if($rec_pos == -1) 
{
print qq!Content-type: text/html\n\n!;
print qq?<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">\n?; 
print qq!<html>\n!;
print qq!<head>\n<title>examen radioamator</title>\n</head>\n!;
print qq!<body bgcolor="#228b22" text="#7fffd4" link="white" alink="white" vlink="white">\n!;
ins_gpl();
print qq!v.3.0.f\n!; #version print for easy upload check
#print qq![$debug_buffer]\n!; #debug
print qq!<br>\n!;
print qq!<br>\n!;
print qq!<h3 align="center">Numele dumneavoastra de utilizator nu se gaseste in baza noastra de date.</h3> <br>\n!;
print qq!<h3 align="center">ATENTIE: Daca ati avut cont si nu mai sunteti in baza de date, inseamna ca nu v-ati mai logat de peste 7 zile, contul se sterge automat. Va rugam consultati manualul.</h3>\n!;
print qq!<form method="link" action="http://localhost/index.html">\n!;
print qq!<center><INPUT TYPE="submit" value="OK"></center>\n!;
print qq!</form>\n!; 
print qq!</body>\n</html>\n!;

close(userFILE) or die("cant close user file\n"); 
exit(); #login was not found in database, no reason to continue
} #.end if
} #.end BLOCK

#BLOCK: time > next_login_time? Login delayed or not?
{
my $act_sec=$utc_time[0];
my $act_min=$utc_time[1];
my $act_hour=$utc_time[2];
my $act_day=$utc_time[3];
my $act_month=$utc_time[4];
my $act_year=$utc_time[5];

my @linesplit;

@linesplit=split(/ /,$slurp_userfile[$rec_pos*7+1]); #linesplit[6] is \n, don't care
chomp $linesplit[5];		#otherwise $linesplit[5]='ab\n'

#ACTION: if(actual_time < next_allowed_login_time) {ERR: wait 5 minutes}

my $truth=1; 
 if($linesplit[5] > $act_year) {$truth=0;}  
 elsif($linesplit[5] == $act_year){
 if($linesplit[4] > $act_month) {$truth=0;} 
 elsif($linesplit[4] == $act_month){
 if($linesplit[3] > $act_day) {$truth=0;}  
 elsif($linesplit[3] == $act_day){
 if($linesplit[2] > $act_hour) {$truth=0;} 
 elsif($linesplit[2] == $act_hour){
 if($linesplit[1] > $act_min) {$truth=0;}  
 elsif($linesplit[1] == $act_min){
 if($linesplit[0] > $act_sec) {$truth=0;}  
 
 } #.end elsif min
 } #.end elsif hour
 } #.end elsif day
 } #.end elsif month
 } #.end elsif year

unless($truth)         #if login is to be delayed
{
print qq!Content-type: text/html\n\n!;
print qq?<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">\n?; 
print qq!<html>\n!;
print qq!<head>\n<title>examen radioamator</title>\n</head>\n!;
print qq!<body bgcolor="#228b22" text="#7fffd4" link="white" alink="white" vlink="white">\n!;
ins_gpl();
print qq!v.3.0.f\n!; #version print for easy upload check
#print qq![$debug_buffer]\n!; #debug
print qq!<br>\n!;
print qq!<br>\n!;
print qq!<h3 align="center">Contul <font color="white">$slurp_userfile[$rec_pos*7]</font> este blocat pentru o perioada de 5 minute pentru incercari repetate cu parola falsa. Mai asteptati.</h3>\n!;
print qq!<form method="link" action="http://localhost/index.html">\n!;
print qq!<center><INPUT TYPE="submit" value="OK"></center>\n!;
print qq!</form>\n!; 
print qq!</body>\n</html>\n!;

close(userFILE) or die("cant close user file\n"); 
exit(); #login must be delayed, no reason to continue
} #.end unless

} #.end BLOCK

#BLOCK: password is correct?
{
my @linesplit;
@linesplit=split(/\n/,$slurp_userfile[$rec_pos*7+2]); #linesplit[1] is \n, don't care

unless($linesplit[0] eq $get_passwd)
{
my $wrong;

print qq!Content-type: text/html\n\n!;
print qq?<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">\n?; 
print qq!<html>\n!;
print qq!<head>\n<title>examen radioamator</title>\n</head>\n!;
print qq!<body bgcolor="#228b22" text="#7fffd4" link="white" alink="white" vlink="white">\n!;
ins_gpl();
print qq!v.3.0.f\n!; #version print for easy upload check
#print qq![$debug_buffer]\n!; #debug
print qq!<br>\n!;
print qq!<br>\n!;

$wrong=$slurp_userfile[$rec_pos*7+3];
chomp $wrong;

if($wrong < 2)
{
#ACTION: increment wrong attempt counter; 3rd mistake blocks the authentication
$wrong++;
$wrong="$wrong\n";
$slurp_userfile[$rec_pos*7+3]=$wrong;
#ACTION: rewrite userfile
truncate(userFILE,0);			#
seek(userFILE,0,0);				#go to beginning of transactionfile
for(my $i=0;$i <= $#slurp_userfile;$i++)
{
printf userFILE "%s",$slurp_userfile[$i]; #we have \n at the end of each element
}
print qq!<h3 align="center">Parola incorecta pentru $slurp_userfile[$rec_pos*7]</h3>\n!;
print qq!<form method="link" action="http://localhost/index.html">\n!;
print qq!<center><INPUT TYPE="submit" value="OK"></center>\n!;
print qq!</form>\n!; 
print qq!</body>\n</html>\n!;

close(userFILE) or die("cant close user file\n"); 
exit(); #password is wrong, no reason to continue
} #.end if
else
{
#ACTION: generate next_login_time
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
my $expire=5;		#5 minutes until next login attempt possible

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

my $entry = "$exp_sec $exp_min $exp_hour $exp_day $exp_month $exp_year\n"; #\n is important

$slurp_userfile[$rec_pos*7+1]=$entry;

#ACTION: reset wrong counter
$wrong="0\n";
$slurp_userfile[$rec_pos*7+3]=$wrong;

#ACTION: rewrite userfile
truncate(userFILE,0);			#
seek(userFILE,0,0);				#go to beginning of transactionfile
for(my $i=0;$i <= $#slurp_userfile;$i++)
{
printf userFILE "%s",$slurp_userfile[$i]; #we have \n at the end of each element
}

print qq!<h3 align="center">Contul $slurp_userfile[$rec_pos*7] este blocat 5 minute din cauza incercarilor repetate de login cu parola falsa.</h3>\n!;
print qq!<form method="link" action="http://localhost/index.html">\n!;
print qq!<center><INPUT TYPE="submit" value="OK"></center>\n!;
print qq!</form>\n!; 
print qq!</body>\n</html>\n!;

close(userFILE) or die("cant close user file\n"); 
exit(); #password is wrong, no reason to continue

} #.end else
} #.end unless
} #.end BLOCK

#BLOCK:Reset expiry
{
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

my $entry = "$exp_sec $exp_min $exp_hour $exp_day $exp_month $exp_year\n"; #\n is important

$slurp_userfile[$rec_pos*7+4]=$entry;

#ACTION: reset wrong counter

$slurp_userfile[$rec_pos*7+3]="0\n";
#UNSTABLE
#ACTION: rewrite userfile
truncate(userFILE,0);			#
seek(userFILE,0,0);				#go to beginning of transactionfile
for(my $i=0;$i <= $#slurp_userfile;$i++)
{
printf userFILE "%s",$slurp_userfile[$i]; #we have \n at the end of each element
}

} #.end BLOCK


#close ar putea sa dispara din necesitatea de a mai scrie penalizari in userfile
#close(userFILE) or die("cant close user file\n");


#BLOCK: refresh transaction file and Generate new transaction id
{
#ACTION: open transaction ID file
open(transactionFILE,"+< sim_transaction") or die("can't open transaction file: $!\n");					#open transaction file for writing
#flock(transactionFILE,2);		#LOCK_EX the file from other CGI instances

#ACTION: generate next transaction
seek(transactionFILE,0,0);		#go to the beginning
@tridfile = <transactionFILE>;		#slurp file into array

$trid=$tridfile[0];
chomp $trid;						#eliminate \n



$trid=hex($trid);		#convert string to numeric


if($trid == 0xFFFFFF) {$tridfile[0] = sprintf("%+06X\n",0);}
else { $tridfile[0]=sprintf("%+06X\n",$trid+1);}                #cyclical increment 000000 to 0xFFFFFF


#ACTION: refresh transaction NON-STANDARD: 
#this will be changed in next version: it will increase the faults instead of dying
my $act_sec=$utc_time[0];
my $act_min=$utc_time[1];
my $act_hour=$utc_time[2];
my $act_day=$utc_time[3];
my $act_month=$utc_time[4];
my $act_year=$utc_time[5];
my @livelist=();
my @linesplit;

#UNSTABLE FROM HERE

unless($#tridfile == 0) 		#unless transaction list is empty (but transaction exists on first line)
{ #.begin unless
  for(my $i=1; $i<= $#tridfile; $i++)	#check all transactions 
  {

   @linesplit=split(/ /,$tridfile[$i]);
   chomp $linesplit[8]; #\n is deleted 
#abandoned own transactions are deleted even if expired or not - abandoned exams are punished
 if($linesplit[1] eq  $get_login) { #for all transactions of the owner...
  if ($linesplit[2] =~ /[4-7]/) #...abandoned(expired or not)exam-transaction
   {   &punishment($linesplit[1]); } # the user will be punished for this
                                  } #
 elsif($linesplit[8] > $act_year) {@livelist=(@livelist, $i);}  #it's alive one more year, keep it in the list
 elsif($linesplit[8] == $act_year){
 if($linesplit[7] > $act_month) {@livelist=(@livelist, $i);}  #it's alive one more month, keep it in the list
 elsif($linesplit[7] == $act_month){
 if($linesplit[6] > $act_day) {@livelist=(@livelist, $i);}  #it's alive one more day, keep it in the list
 elsif($linesplit[6] == $act_day){
 if($linesplit[5] > $act_hour) {@livelist=(@livelist, $i);}  #it's alive one more hour, keep it in the list
 elsif($linesplit[5] == $act_hour){
 if($linesplit[4] > $act_min) {@livelist=(@livelist, $i);}  #it's alive one more minute, keep it in the list
 elsif($linesplit[4] == $act_min){
 if($linesplit[3] > $act_sec) {@livelist=(@livelist, $i);}  #it's alive one more second, keep it in the list
else {
#it's time-expired... 
if ($linesplit[2] =~ /[4-7]/) #...exam-transaction
   {   &punishment($linesplit[1]); } # the user will be punished for this
     } #transaction is expired
 } #.end elsif min
else {
#it's time-expired... 
if ($linesplit[2] =~ /[4-7]/) #...exam-transaction
   {   &punishment($linesplit[1]); } # the user will be punished for this
     } #transaction is expired
 } #.end elsif hour
else {
#it's time-expired... 
if ($linesplit[2] =~ /[4-7]/) #...exam-transaction
   {   &punishment($linesplit[1]); } # the user will be punished for this
     } #transaction is expired
 } #.end elsif day
else {
#it's time-expired... 
if ($linesplit[2] =~ /[4-7]/) #...exam-transaction
   {   &punishment($linesplit[1]); } # the user will be punished for this
     } #transaction is expired
 } #.end elsif month
else {
#it's time-expired... 
if ($linesplit[2] =~ /[4-7]/) #...exam-transaction
   {   &punishment($linesplit[1]); } # the user will be punished for this
     } #transaction is expired

 } #.end elsif year

else {
#it's time-expired... 
if ($linesplit[2] =~ /[4-7]/) #...exam-transaction
   {   &punishment($linesplit[1]); } # the user will be punished for this
     } #transaction is expired


  
  } #.end for

#dupa eventualele penalizari, se actualizeaza si inchide si userFILE
#ACTION: rewrite userfile
truncate(userFILE,0);			#
seek(userFILE,0,0);				#go to beginning of transactionfile
for(my $i=0;$i <= $#slurp_userfile;$i++)
{
printf userFILE "%s",$slurp_userfile[$i]; #we have \n at the end of each element
}

close(userFILE) or die("cant close user file\n");

my @extra=();
@extra=(@extra,$tridfile[0]);		#transactionID it's always alive

my $j;

foreach $j (@livelist) {@extra=(@extra,$tridfile[$j]);}
@tridfile=@extra;

} #.end unless


#print qq!tridfile after refresh: @tridfile[0..$#tridfile]<br>\n!;

#ACTION: generate a new transaction for anonymous

#print qq!generate new transaction<br>\n!;
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
my $entry = "$hexi $get_login 2 $exp_sec $exp_min $exp_hour $exp_day $exp_month $exp_year\n";

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

} #.end BLOCK


print qq!Content-type: text/html\n\n!;
print qq?<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">\n?; 
print qq!<html>\n!;
print qq!<head>\n<title>examen radioamator</title>\n</head>\n!;
print qq!<body bgcolor="#228b22" text="#7fffd4" link="white" alink="white" vlink="white">\n!;
ins_gpl();
print qq!<a name="begin"></a>\n!;
print qq!v.3.0.f\n!; #version print for easy upload check
print qq!<br>\n!;

print qq!<table width="95%" border="1" align="center" cellpadding="7">\n!;
print qq!<tr bgcolor="gray">\n!;
print qq!<td align="center">Rezultatele si datele de contact pentru <font size="+1" color="yellow">$slurp_userfile[$rec_pos*7]</font> </td>\n!;
print qq!</tr>\n!;
print qq!</table>\n!;

#====================V3 code ======================
# undeva aici trebuie sa ma infig
# aici trebuie extras numele userului 
 $hlr_filename = $get_login;
 $hlr_filename =~ s/\//\@slash\@/; # spec char / is replaced

if(-e "hlr/$hlr_filename") 
{
#print qq!exista si deschidem hlr/$hlr_filename<br>\n!; #debug
#deschide hlrfile readonly
open(HLRfile,"<hlr/$hlr_filename") || die("nu se deschideeeee"); #open readonly
#flock(HLRfile,1); #lock shared
seek(HLRfile,0,0); #rewind
$hlrclass=<HLRfile>; #citeste clasa
chomp($hlrclass);
#print qq!are clasa $hlrclass<br>\n!; #debug
if($hlrclass eq 'clasa1') {@materii=("prog_HAREC_radiotehnica","prog_NTSM","prog_HAREC_op","prog_HAREC_reg");
 @strips=("strip_db_tech1","strip_db_ntsm","strip_db_op1","strip_db_legis1");}
elsif($hlrclass eq 'clasa2'){@materii=("prog_HAREC_radiotehnica","prog_NTSM","prog_HAREC_op","prog_HAREC_reg");
@strips=("strip_db_tech2","strip_db_ntsm","strip_db_op2","strip_db_legis2");}
elsif($hlrclass eq 'clasa3'){@materii=("prog_CEPT_Novice_radiotehnica","prog_NTSM","prog_CEPT_Novice_op","prog_CEPT_reg");
@strips=("strip_db_tech3","strip_db_ntsm","strip_db_op3","strip_db_legis3");}
elsif($hlrclass eq 'clasa4'){@materii=("prog_NTSM","prog_CEPT_Novice_op","prog_CEPT_reg");
@strips=("strip_db_ntsm","strip_db_op3r","strip_db_legis3r");}
else {# this else should never be executed
	print qq!Content-type: text/html\n\n!;
	print qq?<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">\n?; 
	print qq!<html>\n!;
	print qq!<head>\n<title>examen radioamator</title>\n</head>\n!;
	print qq!<body bgcolor="#228b22" text="#7fffd4" link="white" alink="white" vlink="white">\n!;
		ins_gpl();
	print qq!v.3.0.f\n!; #version print for easy upload check
	print qq!<br>\n!;
	print qq!<br>\n!;
	print qq!<h3 align="center">This branch should never occur</h3> <br>\n!;
	print qq!<form method="link" action="http://localhost/index.html">\n!;
	print qq!<center><INPUT TYPE="submit" value="OK"></center>\n!;
	print qq!</form>\n!; 
	print qq!</body>\n</html>\n!;
	#please close  whatever is open at the moment
	#tbd
	#close(userFILE) or die("cant close user file\n"); 
	exit(); #hlr database defective, no reason to continue. Exit after ERR page
      }# this else should never be executed

} #.end if -e

#====================.V3 code ======================

print qq!<br>\n!;

print qq!<table width="90%" border="1" align="center" cellpadding="5">\n!;

print qq!<tr bgcolor="gray">\n!;
print qq!<td align="center" width="15%"><font color="white">&nbsp;</font>\n!;
print qq!<td align="center">PAGINA ESTE VALABILA 15 minute.\n!;
print qq!</tr>\n!;

print qq!<tr>\n!;
print qq!<td align="center">login:</td>\n!;
print qq!<td align="center"><font color="yellow">$slurp_userfile[$rec_pos*7]</font></td>\n!; #trial: <font color="blue"> Contul expira la: $slurp_userfile[$rec_pos*11+4]</font>
print qq!</tr>\n!;

print qq!<tr>\n!;
print qq!<td align="center">Tip examen: </td>\n!;

print qq!<td align="center">!;
   if($slurp_userfile[$rec_pos*7+5] eq "0\n") {print qq!Cont de antrenament!;} 
elsif($slurp_userfile[$rec_pos*7+5] eq "1\n") {print qq!Examen clasa I!;} 
elsif($slurp_userfile[$rec_pos*7+5] eq "2\n") {print qq!Examen clasa II!;} 
elsif($slurp_userfile[$rec_pos*7+5] eq "3\n") {print qq!Examen clasa III!;} 
elsif($slurp_userfile[$rec_pos*7+5] eq "4\n") {print qq!Examen clasa III-R!;} 
else{ print qq!cod eronat!;}
print qq!</td>\n!;

print qq!</tr>\n!;

print qq!<tr>\n!;
print qq!<td align="center">Clasa promovata:</td>\n!;

print qq!<td align="center">!;
if($slurp_userfile[$rec_pos*7+6] eq "0\n") {print qq!Niciun examen promovat inca<br><small>Selectati butonul de examen corespunzator</small>!;} 
elsif($slurp_userfile[$rec_pos*7+6] eq "1\n") {print qq!clasa I!;} 
elsif($slurp_userfile[$rec_pos*7+6] eq "2\n") {print qq!clasa II!;} 
elsif($slurp_userfile[$rec_pos*7+6] eq "3\n") {print qq!clasa III!;} 
elsif($slurp_userfile[$rec_pos*7+6] eq "4\n") {print qq!clasa III-R!;} 
elsif($slurp_userfile[$rec_pos*7+6] eq "5\n") {print qq!NEPROMOVAT!;} 
else{ print qq!cod eronat!;}
if($slurp_userfile[$rec_pos*7+5] ne "0\n" && $slurp_userfile[$rec_pos*7+6] ne "0\n" ){
print qq!<br><small>Rezultatul acestui examen ramane blocat pentru a fi vazut de examinator(rolul celui care a creat contul). Pentru alt examen trebuie sa primesti un nou cont de examen sau sa te inregistrezi cu un cont de antrenament</small>!;
    }
print qq!</td>\n!;

print qq!</tr>\n!;

print qq!</table>\n!;

print qq!<br>\n!;

print qq!<table width="90%" border="0" align="center" cellpadding="5">\n!;
print qq!<tr>\n!;

#===== V3 code =====
if((-e "hlr/$hlr_filename") && ($hlrclass eq 'clasa4')) {
print qq!<td align="center" width="23%" bgcolor="red">\n!;}
else {print qq!<td align="center" width="23%">\n!;}
#===== .V3 code =====

#examenul III-R apare doar pentru cont training si oneshot nefolosit
  print qq!<form action="http://localhost/cgi-bin/sim_gen3r.cgi" method="get">\n!;
  print qq!<center><input type="submit" value="EXAM cl.III-R"!;
unless(($slurp_userfile[$rec_pos*7+5] eq "0\n")||(($slurp_userfile[$rec_pos*7+5] eq "4\n")&&($slurp_userfile[$rec_pos*7+6] eq "0\n")))  
 { print qq! disabled="y"!;}  
  print qq!></center>\n!;
#ACTION: inserare transaction ID in pagina HTML
{
my $extra=sprintf("%+06X",$trid);
print qq!<input type="hidden" name="transaction" value="$extra">\n!;
}
print qq!</form>\n!;
print qq!</td>\n!;

#===== V3 code =====
if((-e "hlr/$hlr_filename") && ($hlrclass eq 'clasa3')) {
print qq!<td align="center" width="23%" bgcolor="red">\n!;}
else {print qq!<td align="center" width="23%">\n!;}
#===== .V3 code =====

#examenul III apare doar pentru cont training si oneshot nefolosit

  print qq!<form action="http://localhost/cgi-bin/sim_gen3.cgi" method="get">\n!;
  print qq!<center><input type="submit" value="EXAM cl.III"!;
unless(($slurp_userfile[$rec_pos*7+5] eq "0\n")||(($slurp_userfile[$rec_pos*7+5] eq "3\n")&&($slurp_userfile[$rec_pos*7+6] eq "0\n")))  
 { print qq! disabled="y"!;}  
  print qq!></center>\n!;
#ACTION: inserare transaction ID in pagina HTML
{
my $extra=sprintf("%+06X",$trid);
print qq!<input type="hidden" name="transaction" value="$extra">\n!;
}
print qq!</form>\n!;
print qq!</td>\n!;

#===== V3 code =====
if((-e "hlr/$hlr_filename") && ($hlrclass eq 'clasa2')) {
print qq!<td align="center" width="23%" bgcolor="red">\n!;}
else {print qq!<td align="center" width="23%">\n!;}
#===== .V3 code =====

#examenul II apare doar pentru cont training si oneshot nefolosit

  print qq!<form action="http://localhost/cgi-bin/sim_gen2.cgi" method="get">\n!;
  print qq!<center><input type="submit" value="EXAM cl.II"!;
unless(($slurp_userfile[$rec_pos*7+5] eq "0\n")||(($slurp_userfile[$rec_pos*7+5] eq "2\n")&&($slurp_userfile[$rec_pos*7+6] eq "0\n")))  
 { print qq! disabled="y"!;}  
  print qq!></center>\n!;
#ACTION: inserare transaction ID in pagina HTML
{
my $extra=sprintf("%+06X",$trid);
print qq!<input type="hidden" name="transaction" value="$extra">\n!;
}
print qq!</form>\n!;
print qq!</td>\n!;
#===== V3 code =====
if((-e "hlr/$hlr_filename") && ($hlrclass eq 'clasa1')) {
print qq!<td align="center" width="23%" bgcolor="red">\n!;}
else {print qq!<td align="center" width="23%">\n!;}
#===== .V3 code =====

#examenul cl. I apare doar pentru cont training si oneshot nefolosit
print qq!<form action="http://localhost/cgi-bin/sim_gen1.cgi" method="get">\n!;
print qq!<center><input type="submit" value="EXAM cl.I"!;

unless(($slurp_userfile[$rec_pos*7+5] eq "0\n")||(($slurp_userfile[$rec_pos*7+5] eq "1\n")&&($slurp_userfile[$rec_pos*7+6] eq "0\n")))  
 { print qq! disabled="y"!;}  
  print qq!></center>\n!;
#ACTION: inserare transaction ID in pagina HTML
{
my $extra=sprintf("%+06X",$trid);
print qq!<input type="hidden" name="transaction" value="$extra">\n!;
}
print qq!</form>\n!;
print qq!</td>\n!;


print qq!</tr>\n!;
print qq!</table>\n!;

#print qq!<br>\n!;

print qq!<table width="95%" border="1" align="center" cellpadding="5">\n!;
print qq!<tr>\n!;
print qq!<td>\n!;
print qq!<form method="link" action="http://localhost/index.html">\n!;
print qq!<center><input type="submit" value="IESIRE"></center>\n!;
print qq!</form>\n!; 
print qq!</td>\n!;
print qq!</tr>\n!;
print qq!</table>\n!;


#=============================================V3====
if(-e "hlr/$hlr_filename") {
#afisam legenda
print qq!<br>\n!;
print qq!<font color="yellow">Lupa Convergenta&trade; activata.</font> Daca ramaneti pe aceeasi clasa de autorizare, cu contul de antrenament, programul va monitorizeaza si dirijeaza prin programa. Tine cont de problemele rezolvate, chiar daca examenul ca intreg nu a fost promovat. <br>Astfel la fiecare examinare nu veti mai primi intrebari la care ati raspuns deja corect, va gaseste punctele slabe si insista pe rezolvarea lor.<br>\n!;
print qq!Schimbarea clasei de autorizare sterge acoperirea programei. Daca vrei sa o iei de la inceput cu aceeasi clasa, treci la alta clasa si apoi revii la cea initiala.<br>\n!;
print qq!<br>LEGENDA:<br>\n!;
print qq!<font size="-2">!; 
print qq!<form action="#">\n!;
print qq!La subcapitolul unde nu vezi vreun semn, nu exista intrebari, nici oficiale ale ANCOM, nici de antrenament.<br>\n!; 
#print qq!<input type="radio" value="x" name="y" disabled="y" unchecked="y">Nu exista nicio intrebare la acest subcapitol din programa.<br>\n!;
print qq!<input type="checkbox" value="x" name="y" enabled="y" unchecked="y">Inca nu ai intalnit intrebari din acest subcapitol.<br>\n!;
print qq!<table cellspacing="2"><tr><td bgcolor="red" valign="middle" align="center"><input type="checkbox" value="x" name="y" enabled="y" unchecked="y"></td><td>Aici ai probleme, cel putin o intrebare ai gresit-o, asa ca aici vom insista.</td></tr></table>\n!;
print qq!<input type="checkbox" value="x" name="y" enabled="y" checked="y">Subcapitol stapanit - ai rezolvat toate intrebarile oferite de aici.<br>\n!;
print qq!</form>\n!;

for (my $iter=0; $iter< ($#materii+1); $iter++)
{
#fetch hlr line
$hlrclass = <HLRfile>; #variable reused to fetch the corresponding line from HLR

#print qq!in /hlr avem:$hlrclass<br>\n!; #debug

#load the hash TBD
%hlrline=(); #empty the hash

chomp $hlrclass;
@splitter= split(/,/,$hlrclass);
for (my $split_iter=0; $split_iter<($#splitter/2);$split_iter++)
 {
 %hlrline = (%hlrline,$splitter[$split_iter*2],$splitter[$split_iter*2+1]); #daca linia e stocata direct sub forma de string de hash; 
  } #.end for split iter


print qq!<hr>\n!; #debug
open(stripFILE, "<$strips[$iter]") || die ("cannot open stripfile");
#flock(stripFILE,1);
seek(stripFILE,0,0);
@slurp_strip=<stripFILE>;
close(stripFILE);
my $checkbox_ena;	#flag, checkbox enabled if chapter in programa is covered with at least 
			#one question in database(stripped)
#print qq!stripperi:@slurp_strip<br>\n!; #debug

open (libFILE, "<$materii[$iter]") || die ("cannot open materia");
#flock(libFILE,1);
seek(libFILE,0,0);

#titlul  materiei e pe prima linie
$fileline=<libFILE>;
print qq!<center><font size="+1"><b>$fileline</b></font></center>\n!; #debug

print qq!<font size="-2">!; 
print qq!<form action="#">\n!;
while ($fileline=<libFILE>)	#for each line in programma
{
#==== important V3 code=====TBD
if($fileline =~ /&/)		#active line only
{
	
#@splitter can be reused here;
@splitter = split(/&/,$fileline);
#in $splitter[0] avem codul  de capitol
#in %hlrline avem intrebarile atinse din materie
#verificam prima data daca programa e acoperita cu intrebare
$checkbox_ena="n"; #by default it's disabled
foreach my $slurpline (@slurp_strip)
{
if($slurpline =~ /[A-Z]{1}$splitter[0]/) {$checkbox_ena="y";
#print qq!stripper match:$slurpline $splitter[0]<br>\n!; #debug
}

}#.end foreach

#verificam daca programa e rezolvata
$found='kz';
foreach my $k (keys %hlrline)
{

if($k =~ /[A-Z]{1}$splitter[0]/) {
if(($hlrline{$k} eq 'y') && ($found eq 'kz')) {$found='y'; }
elsif($hlrline{$k} eq 'n'){$found='n'}
#                   print qq!$k = $hlrline{$k}.. $splitter[0]<br>!; #debug
 } #all must be correct for chapter checked
} #.foreach key

#facem afisarea in functie de parametrii $checkbox_ena si $found
#print qq!$checkbox_ena,$found  <br>\n!; #debug

if($found eq 'n') {
print qq!<table cellspacing="2"><tr><td bgcolor="red" valign="middle" align="center">!;
		  }

if($checkbox_ena eq "y")
  { print qq!<input type="checkbox" value="x" name="y" enabled="y" !;

#afisare de check
if (($found eq 'n') || ($found eq 'kz')) {print qq!unchecked="y">!;}
elsif ($found eq 'y') {print qq!checked="y">!;}
 
  }

if($found eq 'n') {
print qq!</td><td>!;
		  }
#tiparim  linia
#if($checkbox_ena eq "y") {
                    print qq!$splitter[1]!;
#                         }

if($found eq 'n') {
print qq!</td></th></table>!;
		  }
else { 
  #if($checkbox_ena eq "y"){ 
  print qq!<br>!;
  #                         }
     }


} #.end if/&/

else {print qq!$fileline<br>!;} #dummy line din programa
#===== .important V3 code
} #.while
print qq!</form>\n!;
print qq!</font>!; #debug

close(libFILE);
print qq!<br>\n<a href="#begin">Sari la inceputul paginii</a>\n!;
} #.end for @materii

# aici vine afisarea programei intregi daca exista history file pentru user

#close hlrfile		#close dupa ce ai marcat prin programe ce e stapanit si ce nu
close(HLRfile);

} #.end if(-e)
else #daca nu are history, afisam ce insemna clasele de autorizare 
{
print qq!<ul>\n!;
print qq!<li>III-R - incepator Restrans; Drept de a opera doar sub supravegherea unui radioamator de clasa III, II sau I.\n!;
print qq!<li>III - incepator; Drept de a lucra in toate benzile.\n!;
print qq!<li>II - avansat; Drept de a opera in toate benzile cu putere sporita.\n!;
print qq!<li>I - avansat; Nivel maxim de putere aprobat, drept de a fi responsabil de statie colectiva.\n!;
print qq!</ul>\n!;
}
#=====.V3 code========
#===== V3 =====
#mai sus trebuie bagata  explicatia ce inseamna fiecare clasa
#=====.V3 =====

print qq!</body>\n</html>\n!;

#---------------------
#punishment subroutine for expired exams
sub punishment($)
{
my $pun_user=$_[0];

#punish the user if it still exists
#1. get position in list
my $user_account=-1;
  for(my $position=0; $position < (($#slurp_userfile+1)/7); $position++)	#check userlist, account by account
  {
if($slurp_userfile[$position*7+0] eq "$pun_user\n") #this is the user record we are interested
{
#begin interested
 $user_account=$position;

$position = ($#slurp_userfile+1)/7; #sfarsitul fortat al ciclului for
} #.end interested
  } #.end for

  #BLOCK: kick in the ass

unless($user_account == -1)
{  
my $failures=$slurp_userfile[$user_account*7+6];
chomp $failures;
my $contype=$slurp_userfile[$user_account*7+5];
chomp $contype;

unless ($contype == 0) {$failures=5;}

$failures="$failures\n";

$slurp_userfile[$user_account*7+6]=$failures; 
} #end unless user exists
} #end 'punishment' sub
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
print qq!Textul intebarilor oficiale publicate de ANCOM face exceptie de la cele de mai sus, nefacand obiectul licentierii GNU GPL,!; 
print qq!modificarea lor si/sau folosirea lor in afara Romaniei in alt mod decat read-only nefiind este permisa. Acest lucru deriva !;
print qq!din faptul ca ANCOM este o institutie publica romana, iar intrebarile publicate au caracter de document oficial.\n!;
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
print qq!Questions marked with ANCOM makes an exception of above-written, as ANCOM is a romanian public authority(similar to FCC in USA)!;
print qq!so any use of the official questions, other than in Read-Only way, is prohibited.\n!; 
print qq!YO6OWN Francisc TOTH, 2008\n!;
print qq!\n!;

print qq!Made in Romania\n!;
print qq+-->\n+;

}