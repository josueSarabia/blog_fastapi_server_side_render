var comments_db = []
var user_db = {}
var blogId = ""

	function showCommentForm() {
		const commentForm = document.getElementById("commentForm")
		commentForm.classList.remove("d-none")
	}

	function saveComment() {
		const saveloading = document.getElementById("saveloadingbutton")
		saveloading.classList.add("spinner-border")
		saveloading.classList.add("spinner-border-sm")

		const cancelloading = document.getElementById("cancelloadingbutton")
		cancelloading.classList.add("spinner-border")
		cancelloading.classList.add("spinner-border-sm")

		const saveCommentButton = document.getElementById("saveCommentButton");
		const cancelCommentButton = document.getElementById("cancelCommentButton");
		saveCommentButton.setAttribute("disabled", "")
		cancelCommentButton.setAttribute("disabled", "")

		const commentTextArea = document.getElementById("commentTextArea");
		commentTextArea.setAttribute("disabled", "")

		const commentTextAreaValue = commentTextArea.value

		fetch("http://localhost:8000/comments/", {
			method: "post",
			headers: {
				"Content-Type": "application/json"
			},
			body: JSON.stringify({
				blog_id: blogId,
				content: commentTextAreaValue
			}),
		}).then(async (response) => {
			let comment = await response.json()
			addCommentToList(comment)
			addEventListeners(comment)
			saveloading.classList.remove("spinner-border")
			saveloading.classList.remove("spinner-border-sm")

			cancelloading.classList.remove("spinner-border")
			cancelloading.classList.remove("spinner-border-sm")

			const commentForm = document.getElementById("commentForm")
			commentForm.classList.add("d-none")

			saveCommentButton.removeAttribute("disabled");
			cancelCommentButton.removeAttribute("disabled");
			commentTextArea.removeAttribute("disabled")
			commentTextArea.value = ""
			
		}).catch((error) => {
			saveloading.classList.remove("spinner-border")
			saveloading.classList.remove("spinner-border-sm")

			cancelloading.classList.remove("spinner-border")
			cancelloading.classList.remove("spinner-border-sm")

			saveCommentButton.removeAttribute("disabled");
			cancelCommentButton.removeAttribute("disabled");
		});
		
	}

	function cancelCommentForm() {
		const commentForm = document.getElementById("commentForm")
		commentForm.classList.add("d-none")

		const commentTextArea = document.getElementById("commentTextArea");
		commentTextArea.value = ""
	}

	function loadComments() {
		fetch(`http://localhost:8000/blogs/${blogId}/comments/`, {
			method: "get",
		}).then(async (response) => {
			comments = await response.json()
			const commentsCol = document.getElementById("commentsCol")
			comments.forEach(comment => {
				addCommentToList(comment)
				addEventListeners()
			});
			
		})
	}

	function getUserInfo() {
		fetch(`http://localhost:8000/users/info/`, {
			method: "get",
		}).then(async (response) => {
			user_db = await response.json()
			loadComments()
		})
	}

	function addCommentToList(comment) {
		comments_db.push(comment)
		let dateComment = new Date(comment.created_at)
		let humanRedableDateComment = dateComment.getDate() +"-"+ (dateComment.getMonth()+1) +"-"+ dateComment.getFullYear()
		let timezoneInHours = dateComment.getTimezoneOffset() / 60
		let humanRedableHoursComment = Math.abs(dateComment.getHours() - timezoneInHours) +":"+( dateComment.getMinutes() < 10 ? "0" : "" ) + dateComment.getMinutes()
		let fullDate = humanRedableDateComment + " " + humanRedableHoursComment

		let html = ""
		
		html += `
			<div id="${comment.id}" class="card">
				<div class="card-body">

					<div class="d-flex flex-start align-items-center">
						<!-- <img class="rounded-circle shadow-1-strong me-3"
							src="https://mdbcdn.b-cdn.net/img/Photos/Avatars/img%20(19).webp" alt="avatar" width="60"
							height="60" /> -->
						<div>
							<h6 class="fw-bold text-primary mb-1">${comment.user.name + " " + comment.user.last_name}</h6>
							<p class="text-muted small mb-0">
								${fullDate}
							</p>
						</div>
			`

			if (user_db.id == comment.user_id) {
				html +=	`
					<div style="margin-left: 10px;">
						<button type="button" id="editCommentButton${comment.id}" class="btn btn-primary">
							<span id="editloadingbutton${comment.id}" class="" ></span>
							Editar
						</button>
						<button type="button" id="deleteCommentButton${comment.id}" class="btn btn-danger">
							<span id="deleteloadingbutton${comment.id}" class="" ></span>
							Eliminar
						</button>
					</div>
				`
			}
			
			html += `
					</div>
					<p id="content${comment.id}" class="mt-3 mb-4 pb-2">
						${comment.content}
					</p>

					<div id="divCommentTextAreaEdit${comment.id}" class="d-flex flex-start w-100 d-none">
						<div class="form-outline w-100">
							<textarea class="form-control" id="commentTextAreaEdit${comment.id}" rows="4"
								style="background: #fff;" placeholder="Escribe..."></textarea>
						</div>
					</div>

					<div id="rowEditFormButtons${comment.id}" class="float-end mt-2 pt-1 d-none">
						<button id="editSaveCommentButton${comment.id}" type="button" class="btn btn-primary btn-sm">
							<span id="editsaveloadingbutton${comment.id}" class="" ></span>
							Guardar
						</button>
						<button id="editCancelCommentButton${comment.id}" type="button" class="btn btn-outline-primary btn-sm">
							<span id="editcancelloadingbutton${comment.id}" class="" ></span>
							Cancelar
						</button>
					</div>
				</div>	
			</div>
		`
		commentsCol.innerHTML += html

	}

	function showEditCommentForm(event) {
		const commentElement = event.target
		const commentId = event.target.id.replace("editCommentButton", "")

		const editCommentButton = document.getElementById("editCommentButton" + commentId);
		const deleteCommentButton = document.getElementById("deleteCommentButton" + commentId);
		editCommentButton.classList.add("d-none")
		deleteCommentButton.classList.add("d-none")

		const content = document.getElementById("content" + commentId);
		content.classList.add("d-none")

		const divCommentTextAreaEdit = document.getElementById("divCommentTextAreaEdit" + commentId);
		divCommentTextAreaEdit.classList.remove("d-none")

		const commentTextAreaEdit = document.getElementById("commentTextAreaEdit" + commentId);
		commentTextAreaEdit.value = content.innerText.trim()

		const rowEditFormButtons = document.getElementById("rowEditFormButtons" + commentId);
		rowEditFormButtons.classList.remove("d-none")
	}

	function saveEditComment(event) {
		const commentElement = event.target
		const commentId = event.target.id.replace("editSaveCommentButton", "")

		const editsaveloadingbutton = document.getElementById("editsaveloadingbutton" + commentId)
		editsaveloadingbutton.classList.add("spinner-border")
		editsaveloadingbutton.classList.add("spinner-border-sm")

		const editcancelloadingbutton = document.getElementById("editcancelloadingbutton" + commentId)
		editcancelloadingbutton.classList.add("spinner-border")
		editcancelloadingbutton.classList.add("spinner-border-sm")

		const editSaveCommentButton = document.getElementById("editSaveCommentButton" + commentId);
		const editCancelCommentButton = document.getElementById("editCancelCommentButton" + commentId);
		editSaveCommentButton.setAttribute("disabled", "")
		editCancelCommentButton.setAttribute("disabled", "")

		const commentTextAreaEdit = document.getElementById("commentTextAreaEdit" + commentId);
		commentTextAreaEdit.setAttribute("disabled", "")

		const commentTextAreaEditValue = commentTextAreaEdit.value

		updatedComment = comments_db.filter(el =>el.id == commentId)[0]
		updatedComment.content = commentTextAreaEditValue


		fetch("http://localhost:8000/comments/", {
			method: "put",
			headers: {
				"Content-Type": "application/json"
			},
			body: JSON.stringify({...updatedComment}),
		}).then(async (response) => {
			editsaveloadingbutton.classList.remove("spinner-border")
			editsaveloadingbutton.classList.remove("spinner-border-sm")
			editcancelloadingbutton.classList.remove("spinner-border")
			editcancelloadingbutton.classList.remove("spinner-border-sm")
			editSaveCommentButton.removeAttribute("disabled")
			editCancelCommentButton.removeAttribute("disabled")
			commentTextAreaEdit.removeAttribute("disabled")

			const editCommentButton = document.getElementById("editCommentButton" + commentId);
			const deleteCommentButton = document.getElementById("deleteCommentButton" + commentId);
			editCommentButton.classList.remove("d-none")
			deleteCommentButton.classList.remove("d-none")

			const content = document.getElementById("content" + commentId);
			content.innerText = commentTextAreaEdit.value.trim()
			content.classList.remove("d-none")

			const divCommentTextAreaEdit = document.getElementById("divCommentTextAreaEdit" + commentId);
			divCommentTextAreaEdit.classList.add("d-none")

			const rowEditFormButtons = document.getElementById("rowEditFormButtons" + commentId);
			rowEditFormButtons.classList.add("d-none")

		})
	}

	function cancelEditComment(event) {
		const commentElement = event.target
		const commentId = event.target.id.replace("editCancelCommentButton", "")

		const editCommentButton = document.getElementById("editCommentButton" + commentId);
		const deleteCommentButton = document.getElementById("deleteCommentButton" + commentId);
		editCommentButton.classList.remove("d-none")
		deleteCommentButton.classList.remove("d-none")

		const content = document.getElementById("content" + commentId);
		content.classList.remove("d-none")

		const divCommentTextAreaEdit = document.getElementById("divCommentTextAreaEdit" + commentId);
		divCommentTextAreaEdit.classList.add("d-none")

		const commentTextAreaEdit = document.getElementById("commentTextAreaEdit" + commentId);
		commentTextAreaEdit.value = content.innerText.trim()


		const rowEditFormButtons = document.getElementById("rowEditFormButtons" + commentId);
		rowEditFormButtons.classList.add("d-none")
	}

	function deleteComment(event) {
		const commentElement = event.target
		const commentId = event.target.id.replace("deleteCommentButton", "")

		const editloadingbutton = document.getElementById("editloadingbutton" + commentId)
		editloadingbutton.classList.add("spinner-border")
		editloadingbutton.classList.add("spinner-border-sm")

		const deleteloadingbutton = document.getElementById("deleteloadingbutton" + commentId)
		deleteloadingbutton.classList.add("spinner-border")
		deleteloadingbutton.classList.add("spinner-border-sm")

		const editCommentButton = document.getElementById("editCommentButton" + commentId);
		const deleteCommentButton = document.getElementById("deleteCommentButton" + commentId);
		editCommentButton.setAttribute("disabled", "")
		deleteCommentButton.setAttribute("disabled", "")

		Swal.fire({
			title: 'Eliminar comentario',
			text: '¿Seguro que desea eliminar este comentario?. Esta acción no es reversible.',
			icon: 'warning',
			confirmButtonText: 'Si, Eliminar.',
			confirmButtonColor: "#dc3545",
			showCancelButton: true,
			cancelButtonText: "No, cancelar.",
			cancelButtonColor: "#3085d6"
		}).then((responseSwal) => {
			
			if (responseSwal.value) {
				fetch("http://localhost:8000/comments/"+commentId, {
					method: "delete",
				}).then(async (response) => {
					const commentsList = document.getElementById("commentsCol");
					const commentElement = document.getElementById(commentId);
					commentsList.removeChild(commentElement)
					let index = comments_db.findIndex(el => el.id == commentId)
					comments_db.splice(index, 1)
				})
			} else {
				editloadingbutton.classList.remove("spinner-border")
				editloadingbutton.classList.remove("spinner-border-sm")
				deleteloadingbutton.classList.remove("spinner-border")
				deleteloadingbutton.classList.remove("spinner-border-sm")
				editCommentButton.removeAttribute("disabled")
				deleteCommentButton.removeAttribute("disabled")
			}
		})

		

	}

	function addEventListeners() {
		comments_db.forEach(el => {
			if (user_db.id == el.user_id) {
				const editCommentButton = document.getElementById("editCommentButton" + el.id)
				editCommentButton.addEventListener('click', function (event) {
					showEditCommentForm(event)
				}, false)

				const deleteCommentButton = document.getElementById("deleteCommentButton" + el.id)
				deleteCommentButton.addEventListener('click', function (event) {
					deleteComment(event)
				}, false)

				const editSaveCommentButton = document.getElementById("editSaveCommentButton" + el.id)
				editSaveCommentButton.addEventListener('click', function (event) {
					saveEditComment(event)
				}, false)

				const editCancelCommentButton = document.getElementById("editCancelCommentButton" + el.id)
				editCancelCommentButton.addEventListener('click', function (event) {
					cancelEditComment(event)
				}, false)
			}
		})
	}

	function load(id) {
		const addcommentbutton = document.getElementById("addcommentbutton")
		addcommentbutton.addEventListener('click', function () {
			showCommentForm()
		}, false)

		const saveCommentButton = document.getElementById("saveCommentButton")
		saveCommentButton.addEventListener('click', function () {
			saveComment()
		}, false)

		const cancelCommentButton = document.getElementById("cancelCommentButton")
		cancelCommentButton.addEventListener('click', function () {
			cancelCommentForm()
		}, false)

		blogId = id
		getUserInfo()

	}
