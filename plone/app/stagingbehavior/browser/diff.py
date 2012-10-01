from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView

from plone.app.iterate.interfaces import IWorkingCopy, IBaseline

from plone.app.stagingbehavior.utils import get_baseline, get_working_copy

class DiffView(BrowserView):

    def __init__( self, context, request ):
        self.context = context
        self.request = request
        if IBaseline.providedBy( self.context ):
            self.baseline = context
            self.working_copy = get_working_copy(context)
        elif IWorkingCopy.providedBy( self.context ):
            self.working_copy = context
            self.baseline = get_baseline(context)
        else:
            raise AttributeError("Invalid Context")

    def diffs( self ):
        diff = getToolByName(self.context, 'portal_diff')
        return diff.createChangeSet( self.baseline,
                                     self.working_copy,
                                     id1="Baseline",
                                     id2="Working Copy" )
