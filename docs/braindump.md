7/7
can have multiple criteria to sort by
criteria -> track's metadata columns

potential supported criteria: loudness, tempo, danceability, acousticness, energy, instrumentalness, key, liveness, loudness, speechiness
- GET /audio-features/{id}

can use ml to auto generate playlist image? could be too costly
can use ml to auto generate a gradient color scheme based on the chosen criteria

OR use a few key features (danceability, energy, can make hyperparams to control weight of each, or even just use one feature if that's too complicated) to create a gradient , then use ML to determine cutoff points (cuz this is the most subjective part. and llm's are good at being subjective). or if thats too complex we can just divide the 0-1 scale for the feature into however many playlist buckets they chose

now for the important part: what aws services shall we use
- rds (relational, store track ids and track features)
- ec2 (compute the gradients)
- bedrock

final polished idea:
- let user decide which features they care about. (energy, valence, danceability) they choose N features
- project chosen features of all liked songs into N-dimensional feature space
- then bin via k-means clustering where k = number of playlists they want
- for all generated cluster/bin, use bedrock to predict what the current combination of feature values (ex high energy, low acousticness), and suggest color gradient scheme for the bins
- or the basic version of this would just be dimensionality reduction into 1d (linearize) and then project onto a rainbow. simple
- optional/alternative to this^ is to use the values and assign to hue, saturation. even more basic. this means we make the features more deterministic