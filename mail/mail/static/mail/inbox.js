document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // Use compose form submit to send the email
  document.querySelector('#compose-form').addEventListener('submit', event => {
    event.preventDefault();
    send_email();
  });

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      // Print emails
      console.log(emails);

      emails.forEach(email => {
        const emailEl = document.createElement('div');
        const senderEl = document.createElement('strong');
        const subjectEl = document.createElement('span');
        const timestampEl = document.createElement('time');

        emailEl.classList.add('list-group-item')

        emailEl.appendChild(senderEl);
        emailEl.appendChild(subjectEl);
        emailEl.appendChild(timestampEl);

        senderEl.innerHTML = email.sender;
        subjectEl.innerHTML = email.subject;
        timestampEl.innerHTML = email.timestamp;

        document.querySelector('#emails-view').appendChild(emailEl);
      });
  });

}

function send_email() {

  // Get recipients, subject and body of an email form compose form input fields
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  // Send a POST request to API to send the email
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients,
        subject,
        body
    })
  })
  .then(response => response.json())
  .then(result => {
      // If the email was successfully sent, load the sent mailbox
      if (result.message) {
        load_mailbox('sent');
      // Else alert the user with error message from API
      } else {
        alert(result.error);
      }
  });
}