#!/usr/local/bin/perl

use strict;
require Suika::CGI;

my %ex_point1 = ();
(
  kokugo	=> 54,
  suugaku	=> 55,
  eigo	=> 57,
  sekaishi	=> 53,
  nihonshi	=> 0,
  chiri	=> 0,
  butsuri	=> 54,
  kagaku	=> 52,
  seibutsu	=> 0,
  _OBJECT	=> 57,
);

my %ex_point2 = ();
(
  kokugo	=> 53,
  suugaku	=> 55,
  eigo	=> 55,
  sekaishi	=> 52,
  nihonshi	=> 0,
  chiri	=> 0,
  butsuri	=> 54,
  kagaku	=> 51,
  seibutsu	=> 0,
  _OBJECT	=> 58,
);

my %ex_haiten1 = ();
(
  kokugo	=> 80,
  suugaku	=> 80,
  eigo	=> 80,
  sekaishi	=> 40,
  nihonshi	=> 0,
  chiri	=> 0,
  butsuri	=> 40,
  kagaku	=> 0,
  seibutsu	=> 0,
);

my %ex_haiten2 = ();
(
  kokugo	=> 0,
  suugaku	=> 300,
  eigo	=> 150,
  sekaishi	=> 0,
  nihonshi	=> 0,
  chiri	=> 0,
  butsuri	=> 150,
  kagaku	=> 150,
  seibutsu	=> 0,
);


sub kanzan (%%%%) {
  my ($point1, $full1, $point2, $full2) = @_;
  my (%kanzaned1, %kanzaned2);
  $$full1{_ALL} = 0;
  for my $subject (keys %$full1) {
    next if $subject =~ /^_/;
    $kanzaned1{$subject} = $$point1{$subject}*$$full1{$subject}/100;
    $kanzaned1{_ALL} += $kanzaned1{$subject};
    $$full1{_ALL} += $$full1{$subject};
  }
  $kanzaned1{_PERCENT} = $$full1{_ALL}==0?0:100*$kanzaned1{_ALL}/$$full1{_ALL};
  $$full2{_ALL} = 0;
  for my $subject (keys %$full2) {
    next if $subject =~ /^_/;
    $kanzaned2{$subject} = $$point2{$subject}*$$full2{$subject}/100;
    $kanzaned2{_ALL} += $kanzaned2{$subject};
    $$full2{_ALL} += $$full2{$subject};
  }
  $kanzaned2{_PERCENT} = $$full2{_ALL}==0?0:100*$kanzaned2{_ALL}/$$full2{_ALL};
  
  my ($percent, $object_percent);
  $percent = ($$full1{_ALL}+$$full2{_ALL})==0?0:
             100*($kanzaned1{_ALL}+$kanzaned2{_ALL})
                /($$full1{_ALL}+$$full2{_ALL});
  $object_percent = ($$full1{_ALL}+$$full2{_ALL})==0?0:
                    ($$point1{_OBJECT}*$$full1{_ALL}
                    +$$point2{_OBJECT}*$$full2{_ALL})
                /($$full1{_ALL}+$$full2{_ALL});
  ($percent, $object_percent, \%kanzaned1, \%kanzaned2);
}

my (%mypoint1, %mypoint2, %haiten1, %haiten2);
if ($Suika::CGI::param{newform} ne 'no') {
  %mypoint1 = %ex_point1;
  %mypoint2 = %ex_point2;
  %haiten1 = %ex_haiten1;
  %haiten2 = %ex_haiten2;
} else {
  for my $s (keys %Suika::CGI::param) {
    $mypoint1{$1} = $Suika::CGI::param{$s} if $s =~ /^(.+[^H_])1$/;
    $mypoint2{$1} = $Suika::CGI::param{$s} if $s =~ /^(.+[^H_])2$/;
    $mypoint1{'_'.$1} = $Suika::CGI::param{$s} if $s =~ /^(.+)_1$/;
    $mypoint2{'_'.$1} = $Suika::CGI::param{$s} if $s =~ /^(.+)_2$/;
    $haiten1{$1} = $Suika::CGI::param{$s} if $s =~ /^(.+)H1$/;
    $haiten2{$1} = $Suika::CGI::param{$s} if $s =~ /^(.+)H2$/;
  }
}
my ($percent, $object, $kanzan1, $kanzan2)
 = kanzan ({%mypoint1} => {%haiten1}, {%mypoint2} => {%haiten2});

print STDOUT "Content-Type: text/html; charset=euc-jp
Content-Style-Type: text/css
Content-Language: ja

";
output_html (\%mypoint1 => \%haiten1 => $kanzan1,
             \%mypoint2 => \%haiten2 => $kanzan2,
             percent => $percent, object => $object);

sub diffmark ($) {
  my $diff = shift;
  return '��' if $diff < -4;
  return '��' if $diff < -2;
  return '��' if $diff < 0;
  return '��';
}

sub output_html (%%%%%) {
  my ($p1 => $h1 => $k1, $p2 => $h2 => $k2, %misc) = @_;
  for my $n ($$k1{_PERCENT}, $$k2{_PERCENT}, $misc{percent}, $misc{object}) {
    $n = int ($n);
  }
  $$k1{_DIFF} = $$k1{_PERCENT}-$$p1{_OBJECT};
  $$k2{_DIFF} = $$k2{_PERCENT}-$$p2{_OBJECT};
  $misc{_DIFF} = $misc{percent}-$misc{object};
  $$k1{_DIFFMARK} = diffmark ($$k1{_DIFF});
  $$k2{_DIFFMARK} = diffmark ($$k2{_DIFF});
  $misc{_DIFFMARK} = diffmark ($misc{_DIFF});
  print <<EOH;
<!DOCTYPE html PUBLIC "-//W3D//DTD HTML 4.01//EN">
<html lang="ja">
<head>
<title>��������</title>
<link rev="made" href="mailto:w\@suika.fam.cx">
<link rel="contents" href="http://tomikou.net/">
<link rel="contents" href="/chuubu/">
<style type="text/css">
input	{width: 3em}
</style>
</head>
<body>
<h1>��������</h1>
<form action="kanzan" method="post" accept-charset="iso-2022-jp, iso-2022-jp-3">
<table>
<thead>
<tr>
<th colspan="2">����</th>
<th>���</th><th>����</th><th>�Ѹ�</th>
<th>������</th><th>���ܻ�</th><th>����</th>
<th>ʪ��</th><th>����</th><th>��ʪ</th>
</tr>
</thead>
<tbody>
<tr>
<th rowspan="3">�켡</th><th>������</th>
<td><input type="text" name="kokugo1" value="$$p1{kokugo}"></td>
<td><input type="text" name="suugaku1" value="$$p1{suugaku}"></td>
<td><input type="text" name="eigo1" value="$$p1{eigo}"></td>
<td><input type="text" name="sekaishi1" value="$$p1{sekaishi}"></td>
<td><input type="text" name="nihonshi1" value="$$p1{nihonshi}"></td>
<td><input type="text" name="chiri1" value="$$p1{chiri}"></td>
<td><input type="text" name="butsuri1" value="$$p1{butsuri}"></td>
<td><input type="text" name="kagaku1" value="$$p1{kagaku}"></td>
<td><input type="text" name="seibutsu1" value="$$p1{seibutsu}"></td>
</tr>
<tr>
<th>����</th>
<td><input type="text" name="kokugoH1" value="$$h1{kokugo}"></td>
<td><input type="text" name="suugakuH1" value="$$h1{suugaku}"></td>
<td><input type="text" name="eigoH1" value="$$h1{eigo}"></td>
<td><input type="text" name="sekaishiH1" value="$$h1{sekaishi}"></td>
<td><input type="text" name="nihonshiH1" value="$$h1{nihonshi}"></td>
<td><input type="text" name="chiriH1" value="$$h1{chiri}"></td>
<td><input type="text" name="butsuriH1" value="$$h1{butsuri}"></td>
<td><input type="text" name="kagakuH1" value="$$h1{kagaku}"></td>
<td><input type="text" name="seibutsuH1" value="$$h1{seibutsu}"></td>
</tr>
<tr>
<th>������</th>
<td>$$k1{kokugo}</td><td>$$k1{suugaku}</td><td>$$k1{eigo}</td>
<td>$$k1{sekaishi}</td><td>$$k1{nihonshi}</td><td>$$k1{chiri}</td>
<td>$$k1{butsuri}</td><td>$$k1{kagaku}</td><td>$$k1{seibutsu}</td>
</tr>

<tr>
<th rowspan="3">��</th><th>������</th>
<td><input type="text" name="kokugo2" value="$$p2{kokugo}"></td>
<td><input type="text" name="suugaku2" value="$$p2{suugaku}"></td>
<td><input type="text" name="eigo2" value="$$p2{eigo}"></td>
<td><input type="text" name="sekaishi2" value="$$p2{sekaishi}"></td>
<td><input type="text" name="nihonshi2" value="$$p2{nihonshi}"></td>
<td><input type="text" name="chiri2" value="$$p2{chiri}"></td>
<td><input type="text" name="butsuri2" value="$$p2{butsuri}"></td>
<td><input type="text" name="kagaku2" value="$$p2{kagaku}"></td>
<td><input type="text" name="seibutsu2" value="$$p2{seibutsu}"></td>
</tr>
<tr>
<th>����</th>
<td><input type="text" name="kokugoH2" value="$$h2{kokugo}"></td>
<td><input type="text" name="suugakuH2" value="$$h2{suugaku}"></td>
<td><input type="text" name="eigoH2" value="$$h2{eigo}"></td>
<td><input type="text" name="sekaishiH2" value="$$h2{sekaishi}"></td>
<td><input type="text" name="nihonshiH2" value="$$h2{nihonshi}"></td>
<td><input type="text" name="chiriH2" value="$$h2{chiri}"></td>
<td><input type="text" name="butsuriH2" value="$$h2{butsuri}"></td>
<td><input type="text" name="kagakuH2" value="$$h2{kagaku}"></td>
<td><input type="text" name="seibutsuH2" value="$$h2{seibutsu}"></td>
</tr>
<tr>
<th>������</th>
<td>$$k2{kokugo}</td><td>$$k2{suugaku}</td><td>$$k2{eigo}</td>
<td>$$k2{sekaishi}</td><td>$$k2{nihonshi}</td><td>$$k2{chiri}</td>
<td>$$k2{butsuri}</td><td>$$k2{kagaku}</td><td>$$k2{seibutsu}</td>
</tr>
</tbody>
</table>

<table>
<thead>
<tr>
<th></th><th>����Ψ</th><th>��ɸ��</th><th colspan="2">��</th>
</tr>
</thead>
<tbody>
<tr>
<th>�켡</th>
<td>$$k1{_PERCENT}</td>
<td><input type="text" name="OBJECT_1" value="$$p1{_OBJECT}"></td>
<td>$$k1{_DIFF}</td>
<td>$$k1{_DIFFMARK}</td>
</tr>
<tr>
<th>��</th>
<td>$$k2{_PERCENT}</td>
<td><input type="text" name="OBJECT_2" value="$$p2{_OBJECT}"></td>
<td>$$k2{_DIFF}</td>
<td>$$k2{_DIFFMARK}</td>
</tr>
<tr>
<th>���</th>
<td>$misc{percent}</td>
<td>$misc{object}</td>
<td>$misc{_DIFF}</td>
<td>$misc{_DIFFMARK}</td>
</tr>
</tbody>
</table>

<p>
<input type="hidden" name="newform" value="no">
<input type="submit" value="OK">
</p>
</form>

<div class="navigation">
[<a href="/gate/cvs/perl/kanzan/" xml:lang="en">source</a>]
</div>
</body>
</html>
EOH
}

=head1 LICENSE

Copyright 2001-2002 wakaba E<lt>w@suika.fam.cxE<gt>.

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; see the file COPYING.  If not, write to
the Free Software Foundation, Inc., 59 Temple Place - Suite 330,
Boston, MA 02111-1307, USA.

=cut

1;	# $Date: 2002/09/04 09:02:38 $
### kanzan.cgi ends here
