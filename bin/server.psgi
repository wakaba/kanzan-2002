# -*- perl -*-
use strict;
use warnings;
use Wanage::HTTP;
use Warabe::App;

use Kanzan;

$ENV{LANG} = 'C';
$ENV{TZ} = 'UTC';

return sub {
  my $http = Wanage::HTTP->new_from_psgi_env ($_[0]);
  my $app = Warabe::App->new_from_http ($http);

  return $app->execute_by_promise (sub {
    my $path = $app->path_segments;

    $http->set_response_header
        ('Strict-Transport-Security' => 'max-age=2592000; includeSubDomains; preload');

    return Kanzan->main ($app, $path, undef);
  });
};

=head1 LICENSE

Copyright 2015-2022 Wakaba <wakaba@suikawiki.org>.

This library is free software; you can redistribute it and/or modify
it under the same terms as Perl itself.

=cut
