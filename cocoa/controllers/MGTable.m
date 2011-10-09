/* 
Copyright 2011 Hardcoded Software (http://www.hardcoded.net)

This software is licensed under the "BSD" License as described in the "LICENSE" file, 
which should be included with this package. The terms are also available at 
http://www.hardcoded.net/licenses/bsd_license
*/

#import "MGTable.h"
#import "Utils.h"

@implementation MGTable
- (id)initWithPyClassName:(NSString *)aClassName pyParent:(id)aPyParent view:(MGTableView *)aTableView
{
    self = [super initWithPyClassName:aClassName pyParent:aPyParent view:aTableView];
    columns = [[HSColumns alloc] initWithPyParent:[self py] tableView:aTableView];
    return self;
}

- (id)initWithPy:(id)aPy view:(MGTableView *)aTableView
{
    self = [super initWithPy:aPy view:aTableView];
    columns = [[HSColumns alloc] initWithPyParent:[self py] tableView:aTableView];
    return self;
}

- (void)dealloc
{
    [columns release];
    [super dealloc];
}

/* MGTableView delegate */
- (NSIndexSet *)selectedIndexes
{
    return [Utils array2IndexSet:[[self py] selectedRows]];
}

- (BOOL)tableView:(NSTableView *)tableView shouldEditTableColumn:(NSTableColumn *)column row:(NSInteger)row
{
    return NO;
}

- (NSString *)dataForCopyToPasteboard
{
    return [[self py] selectionAsCSV];
}

/* Public */
- (PyTable *)py
{
    return (PyTable *)py;
}

- (MGTableView *)tableView
{
    return (MGTableView *)tableView;
}

- (HSColumns *)columns
{
    return columns;
}
@end
