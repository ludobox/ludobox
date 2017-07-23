
let contributor = {
  "add_game" : true,
  "edit_game" : true,
  "delete_own_game" : false,
  "delete_others_game" : false
}

let acl = {
  contributor
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
