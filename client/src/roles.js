
let editor = {
  "add_game" : true,
  "edit_game" : true,
  "validate_game" : true,
  "reject_game" : true,
  "back_to_review_game" : true,
  "delete_game" : true
}

let contributor = {
  "add_game" : true,
  "edit_game" : true,
  "delete_own_game" : false,
  "delete_others_game" : false,
  "validate_game" : false,
  "reject_game" : false,
  "back_to_review_game" : false
}

let acl = {
  contributor,
  editor
}

export function isAuthorized(action, user) {

  // unlogged user has no rights
  if (!user.is_auth)
    return false

  let { roles } = user

  // superuser have all rights
  if ( roles.includes("superuser") )
    return true
  else {
    if (roles.indexOf("editor") > -1)
      return acl["editor"][action]
    else
      return acl["contributor"][action]
  }
}
