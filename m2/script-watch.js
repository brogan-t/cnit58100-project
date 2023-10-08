window.onload = function(){
	// Obtain necessary references
	const btnSubmitComment = document.getElementById("submit-comment");
	const txtSubmitComment = document.getElementById("submit-comment-text");
	const divCommentPrefab = document.getElementById("comment-prefab");
	
	const btnExpandDesc = document.getElementById("expand-description");
	const txtDescShort = document.getElementById("video-player-description-short");
	const txtDescLong = document.getElementById("video-player-description-long");
	
	// Add event listener to comment button
	btnSubmitComment.addEventListener("click", function() {
		let newComment = divCommentPrefab.children[0].cloneNode(true);
		newComment.children[1].innerHTML = txtSubmitComment.value;
		divCommentPrefab.parentElement.append(newComment);
		window.scrollTo(0, document.body.scrollHeight);
	});
	
	// Add event listener to description expansion button
	btnExpandDesc.addEventListener("click", function() {
		txtDescShort.style.display = 'none';
		txtDescLong.style.display = 'block';
	});
}