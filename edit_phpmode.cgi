#!/usr/local/bin/perl
# Show web and PHP options for a virtual server

require './virtual-server-lib.pl';
&ReadParse();
$d = &get_domain($in{'dom'});
&can_edit_domain($d) || &error($text{'edit_ecannot'});
&can_edit_phpmode($d) || &error($text{'phpmode_ecannot'});

&ui_print_header(&domain_in($d), $text{'phpmode_title'}, "");

print &ui_form_start("save_phpmode.cgi");
print &ui_hidden("dom", $d->{'id'}),"\n";
print &ui_table_start($text{'phpmode_header'}, undef, 2, [ "width=30%" ]);

# Use suexec
print &ui_table_row(&hlink($text{'phpmode_suexec'}, "phpmode_suexec"),
		    &ui_yesno_radio("suexec", &get_domain_suexec($d)));

# PHP execution mode
@modes = &supported_php_modes($d);
print &ui_table_row(&hlink($text{'phpmode_mode'}, "phpmode"),
		    &ui_radio("mode", &get_domain_php_mode($d),
			      [ map { [ $_, $text{'phpmode_'.$_}."<br>" ] }
				    @modes ]));

# PHP fcgi sub-processes
if (&indexof("fcgid", @modes) >= 0) {
	$children = &get_domain_php_children($d);
	if ($children >= 0) {
		print &ui_table_row(&hlink($text{'phpmode_children'},
					   "phpmode_children"),
				    &ui_opt_textbox("children", $children || '',
					 5, $text{'tmpl_phpchildrennone'}));
		}
	}

# Ruby execution mode
@rubys = &supported_ruby_modes($d);
if (@rubys) {
	print &ui_table_row(&hlink($text{'phpmode_rubymode'}, "rubymode"),
		    &ui_radio("rubymode", &get_domain_ruby_mode($d),
			      [ [ "", $text{'phpmode_noruby'}."<br>" ],
				map { [ $_, $text{'phpmode_'.$_}."<br>" ] }
				    @rubys ]));
	}

# Write logs via program
print &ui_table_row(&hlink($text{'newweb_writelogs'}, "template_writelogs"),
		    &ui_yesno_radio("writelogs", &get_writelogs_status($d)));

print &ui_table_end();
print &ui_form_end([ [ "save", $text{'save'} ] ]);

&ui_print_footer(&domain_footer_link($d),
		 "", $text{'index_return'});

