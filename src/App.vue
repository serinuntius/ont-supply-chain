<template>
  <div id="app">

    <nav class="navbar" role="navigation" aria-label="main navigation">
      <div class="navbar-brand">
        <a class="navbar-item" href="https://bulma.io">
          <img src="https://bulma.io/images/bulma-logo.png" width="112" height="28">
        </a>

        <a role="button" class="navbar-burger burger" aria-label="menu" aria-expanded="false"
           data-target="navbarBasicExample">
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </a>
      </div>

      <div id="navbarBasicExample" class="navbar-menu">
        <div class="navbar-start">
          <a class="navbar-item">
            Home
          </a>

          <a class="navbar-item">
            Documentation
          </a>

          <div class="navbar-item has-dropdown is-hoverable">
            <a class="navbar-link">
              More
            </a>

            <div class="navbar-dropdown">
              <a class="navbar-item">
                About
              </a>
              <a class="navbar-item">
                Jobs
              </a>
              <a class="navbar-item">
                Contact
              </a>
              <hr class="navbar-divider">
              <a class="navbar-item">
                Report an issue
              </a>
            </div>
          </div>
        </div>

        <div class="navbar-end">
          <div class="navbar-item">
            <div class="buttons">
              <a class="button is-primary">
                <strong>Sign up</strong>
              </a>
              <a class="button is-light">
                Log in
              </a>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <div id="role-selector" class="columns is-mobile">
      <div class="column has-text-centered">
        <button class="button is-info is-outlined">Producer</button>
      </div>
      <div class="column has-text-centered">
        <button class="button is-info is-outlined">Super Market</button>
      </div>
      <div class="column has-text-centered">
        <button class="button is-info is-outlined">Customer</button>
      </div>
    </div>
    <div class="columns">
      <div class="column is-12">
      </div>
    </div>

    <div class="columns is-mobile">
      <div class="column has-text-centered">
        <button class="button is-primary">
         <span id="camera-icon">
           <i class="fas fa-camera"></i>
         </span> Scan
          <input type=file accept="image/*" capture=environment @onclick="openCamera(this)" onchange="" tabindex=-1>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
  /* eslint-disable no-undef */

  export default {
    name: 'app',
    methods: {
      openCamera (node) {
        const reader = new FileReader()
        reader.onload = function () {
          qrcode.callback = function (res) {
            if (res instanceof Error) {
              alert("No QR code found. Please make sure the QR code is within the camera's frame and try again.")
            } else {
              alert(res)
            }
          }
          qrcode.decode(reader.result)
        }
        reader.readAsDataURL(node.files[0])
      }
    }
  }
</script>

<style scoped>
  #role-selector {
    padding-top: 30px;
  }

  #camera-icon {
    padding-right: 15px;
  }
</style>

