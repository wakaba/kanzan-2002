package Kanzan;
use strict;
use warnings;
use Path::Tiny;
use Promised::Command;

my $RootPath = path (__FILE__)->parent->parent->absolute;
my $Intro = $RootPath->child ('intro.ja.html')->slurp;

sub main ($$$;$) {
  my ($class, $app, $path, $perl_path) = @_;
  
    if (@$path == 1 and
        ($path->[0] eq '' or
         $path->[0] eq 'intro' or
         $path->[0] eq 'intro.ja' or
         $path->[0] eq 'intro.ja.html')) {
      $app->http->set_response_header
          ('Content-Type' => 'text/html; charset=iso-2022-jp');
      $app->http->send_response_body_as_ref (\$Intro);
      return $app->http->close_response_body;
    } elsif (@$path == 1 and $path->[0] eq 'kanzan') {
      my $cmd = Promised::Command->new ([$perl_path || $RootPath->child ('perl'), $RootPath->child ('kanzan.cgi')]);
      $cmd->envs->{REQUEST_METHOD} = $app->http->request_method;
      $cmd->envs->{QUERY_STRING} = $app->http->original_url->{query};
      $cmd->envs->{CONTENT_LENGTH} = $app->http->request_body_length;
      $cmd->envs->{CONTENT_TYPE} = $app->http->get_request_header ('Content-Type');
      $cmd->stdin ($app->http->request_body_as_ref);
      $cmd->stdout (\my $stdout);
      return $cmd->run->then (sub {
        return $cmd->wait;
      })->then (sub {
        die $_[0] unless $_[0]->exit_code == 0;
        my ($headers, $body) = split /\x0D?\x0A\x0D?\x0A/, $stdout, 2;
        for (split /[\x0D\x0A]/, $headers) {
          if (/^([^\s:]+):(.*)$/) {
            $app->http->add_response_header ($1 => $2);
          } else {
            die "Bad header |$_|";
          }
        }
        $app->http->send_response_body_as_ref (\$body);
        $app->http->close_response_body;
      });
    }

  return $app->send_error (404);
} # main

1;

=head1 LICENSE

Copyright 2015-2022 Wakaba <wakaba@suikawiki.org>.

This library is free software; you can redistribute it and/or modify
it under the same terms as Perl itself.

=cut
