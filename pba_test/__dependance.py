# import sys
#
# # this is a pointer to the module object instance itself.
# this = sys.modules[__name__]
#
# # we can explicitly make assignments on it
# this.dependancies = None
#
# def initialize():
#     if (this.dependancies is None):
#         # also in local function scope. no scope specifier like global is needed
#         this.dependancies = {}
#         # also the name remains free for local use
#         dependancies = "Locally scoped dependancies variable. Doesn't do anything here."
#     else:
#         msg = "Database is already initialized to {0}."
#         raise RuntimeError(msg.format(this.dependancies))
