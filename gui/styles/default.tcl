# gui/styles/default.tcl
# Minimal ttk style tweaks — Windows will use native widgets.
# You can expand this to set fonts/colors for the app.

package require ttk

ttk::style configure TButton -padding {6 3}
ttk::style configure TLabel -padding {2 2}
ttk::style configure Treeview -rowheight 22
