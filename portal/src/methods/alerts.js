let callbacks = [];

export function onFlash(callback) {
    callbacks.push(callback)
}

export function flash(text, type) {
    if (type === undefined)
        type = "primary"

    let alertObj = {
        type,
        text
    }

    callbacks.forEach(cb => cb(alertObj))
}