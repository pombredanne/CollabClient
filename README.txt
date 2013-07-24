Wrapper for common commands in code collaborator

	from collab.CodeCollab import CodeCollabClient
	cc = CodeCollabClient()
	reviewid = cc.create_collab('My code review', 'A little bit of code to make you scratch your head')
	with open('diff_file.diff', 'r') as f:
		cc.add_diffs(reviewid, f.read())
	cc.add_reviewers(reviewid, 'hacker', 'hackreviewer,jobreviewer')
	
Pretty much it.

Test

