window.onload = function(){
	// Obtain necessary references
	const btnSubmitComment = document.getElementById("submit-comment");
	const txtSubmitComment = document.getElementById("submit-comment-text");
	const divCommentPrefab = document.getElementById("comment-prefab");
	
	const txtDescShort = document.getElementById("video-player-description-short");
	const txtDescLong = document.getElementById("video-player-description-long");
	
	// Add event listener to comment button
	if (btnSubmitComment != null) {
		btnSubmitComment.addEventListener("click", function() {
			let newComment = divCommentPrefab.children[0].cloneNode(true);
			newComment.children[1].innerHTML = txtSubmitComment.value;
			//divCommentPrefab.parentElement.append(newComment); // Used to add comments to the bottom, now sorted by date
			divCommentPrefab.after(newComment);
			//window.scrollTo(0, document.body.scrollHeight); // Comments are no longer added to the bottom
		});
	}
	
	// Generate the short description
	
	if (txtDescLong.innerText.length > 140) {
		txtDescShort.innerHTML = txtDescLong.innerText.substring(0, 80) + "... <button id=\"expand-description\" class=\"link\">more</button>";
		const btnExpandDesc = document.getElementById("expand-description");
		// Add event listener to description expansion button
		btnExpandDesc.addEventListener("click", function() {
			txtDescShort.style.display = 'none';
			txtDescLong.style.display = 'block';
		});
	} else {
		txtDescShort.innerHTML = txtDescLong.innerText;
	}
	
	
}